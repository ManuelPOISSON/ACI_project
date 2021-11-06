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
def write_db(conn, cursor):
    # insert information
    # examples of correct requests :
    now = datetime.datetime.now()
    try:
        cursor.execute(
            "INSERT INTO coordinates (id, latitude, longitude) VALUES (?, ?, ?)",
            (1, 52.1168517, 2.6652337),
        )
        cursor.execute(
            "INSERT INTO devices (id, current_coordinates) VALUES (?, ?)",
            (1, 1),
        )
        cursor.execute(
            "INSERT INTO noise_levels (datetime, device, coordinate, noise_level) VALUES (?, ?, ?, ?)",
            (now, 1, 1, 0.45),
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"mariadb Error: {e}")


def read_mean_values(cursor, start, end):
    cursor.execute(
        "SELECT SQL_NO_CACHE latitude, longitude, avg(noise_level) as level FROM coordinates, noise_levels WHERE noise_levels.coordinate = coordinates.id AND datetime > ? AND datetime <= ? "
        "GROUP BY coordinates.id",
        (start, end)
    )
