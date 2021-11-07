import random
from typing import Dict, Union
import mariadb
import datetime

# TODO: find better parameters management
connection_parameters = {
    "user": "user",
    "password": "password",
    "host": "db",
    "database": "soundfog",
    "port": 3306,
}


def setup_database(cursor):
    print("Setup database", flush=True)
    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS coordinates (id INT NOT NULL AUTO_INCREMENT, latitude DOUBLE NOT NULL, longitude DOUBLE NOT NULL,"
            "PRIMARY KEY (id),"
            "UNIQUE (latitude, longitude))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS devices (id INT NOT NULL AUTO_INCREMENT, current_coordinates INT NOT NULL,"
            "PRIMARY KEY (id),"
            "FOREIGN KEY (current_coordinates) REFERENCES coordinates (id))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS noise_levels (datetime DATETIME NOT NULL, device INT NOT NULL, coordinate INT NOT NULL, noise_level FLOAT NOT NULL,"
            "PRIMARY KEY (datetime, device),"
            "FOREIGN KEY (device) REFERENCES devices (id) ON DELETE CASCADE,"
            "FOREIGN KEY (coordinate) REFERENCES coordinates (id),"
            "INDEX (datetime))"
        )
    except mariadb.Error as e:
        print(f"Error: {e}")


def connect(parameters: Dict[str, Union[str, int]]):
    try:
        # Establish a connection
        connection = mariadb.connect(**parameters)
        # Get Cursor
        cur = connection.cursor()
        return connection, cur
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")


# Write test data
def write_fake_noise_level(conn, cursor):
    now = datetime.datetime.now()
    try:
        now_first_sec = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        for time_shift in range(0, 24):
            time = now_first_sec + datetime.timedelta(hours=time_shift)

            for device_id in range(5, 9):
                cursor.execute(
                    "INSERT INTO noise_levels (datetime, device, coordinate, noise_level) VALUES (?, ?, ?, ?)",
                    (time, device_id, device_id, random.uniform(0, 0.05)*100),
                )
        conn.commit()
    except mariadb.Error as e:
        print(f"mariadb Error: {e}")


def write_fake_device(conn, cursor):
    devices_data = (
        (5, 48.1168517, -1.6652337),
        (6, 48.0968517, -1.6452337),
        (7, 48.1368517, -1.6952337),
        (8, 48.1268517, -1.6052337)
    )
    try:

        # insert coordinates
        for coord in devices_data:
            cursor.execute(
                "INSERT INTO coordinates (id, latitude, longitude) VALUES (?, ?, ?)",
                coord,
            )
        conn.commit()
        # insert devices
        for coord in devices_data:
            cursor.execute(
                "INSERT INTO devices (id, current_coordinates) VALUES (?, ?)",
                (coord[0], coord[0]),
            )
        conn.commit()
    except mariadb.Error as e:
        print(f"mariadb write_fake_device Error: {e}")


def delete_fake_data(conn, cursor):
    try:
        cursor.execute(
            "DELETE FROM devices WHERE id >= 5"
        )
        conn.commit()
        cursor.execute(
            "DELETE FROM coordinates WHERE id >= 5"
        )
        conn.commit()
        cursor.execute(
            "DELETE FROM noise_levels WHERE device >= 5"
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"mariadb delete_fake_device Error: {e}")


def write_amplitude(conn, cursor, date, device_id: int, coordinate_id: int, noise_lvl: float):
    try:
        cursor.execute(
            "INSERT INTO noise_levels (datetime, device, coordinate, noise_level) VALUES (?, ?, ?, ?)",
            (date, device_id, coordinate_id, noise_lvl),
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"error while writing amplitude: {e}")


def read_mean_values(cursor, start, end):
    cursor.execute(
        "SELECT SQL_NO_CACHE latitude, longitude, avg(noise_level) as level FROM coordinates, noise_levels WHERE noise_levels.coordinate = coordinates.id AND datetime > ? AND datetime <= ? "
        "GROUP BY coordinates.id",
        (start, end)
    )


def print_bd(cursor):
    cursor.execute(
        "SELECT * FROM coordinates"
    )
    ret = "COORDINATES \n"
    for data_tuple in cursor:
        ret += str(data_tuple) + "\n"
    cursor.execute(
        "SELECT * FROM devices"
    )
    ret += "DEVICES \n"
    for data_tuple in cursor:
        ret += str(data_tuple) + "\n"
    ret += "NOISE_LEVELS \n"
    cursor.execute(
        "SELECT * FROM noise_levels"
    )
    for data_tuple in cursor:
        ret += str(data_tuple) + "\n"
    print(ret)
    return ret
