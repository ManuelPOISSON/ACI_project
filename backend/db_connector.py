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
            "CREATE TABLE IF NOT EXISTS rpi(rpi_id int, latitude float, longitude float,"
            "PRIMARY KEY (rpi_id))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS noises_levels(rpi_id int, noise_level int, datetime DateTime,"
            "PRIMARY KEY (rpi_id, datetime),"
            "FOREIGN KEY (rpi_id) REFERENCES rpi(rpi_id))"
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


def write_db(conn, cursor):
    # insert information
    # example of correct request :
    # INSERT INTO `rpi` (`rpi_id`, `latitude`, `longitude`) VALUES ('2', '52.1168517', '2.6652337');
    now = datetime.datetime.now()
    try:
        cursor.execute(
            "INSERT INTO rpi (rpi_id, latitude, longitude) VALUES (?, ?, ?)",
            ("3", "1.0", "-1.0"),
        )
        cursor.execute(
            "INSERT INTO noises_levels (rpi_id, noise_level, datetime) VALUES (?, ?, ?)",
            ("3", "2", f"{now}"),
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

def read_db(cursor):
    cur = cursor
    # retrieving information
    rpi_id = 3
    cur.execute("SELECT latitude, longitude FROM rpi WHERE rpi_id=?", (rpi_id,))

    for latitude, longitude in cur:
        print(f"lat: {latitude}, long: {longitude}")
