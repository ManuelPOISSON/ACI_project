# Module Imports
from typing import Dict, Union

import mariadb
import sys
import datetime


def setup_database(cursor):
    try:
        cursor.execute("CREATE TABLE rpi(rpi_id int, latitude float, longitude float,"
                       "PRIMARY KEY (rpi_id))")
        cursor.execute("CREATE TABLE noises_levels(rpi_id int, noise_level int, datetime DateTime,"
                       "PRIMARY KEY (rpi_id, datetime),"
                       "FOREIGN KEY (rpi_id) REFERENCES rpi(rpi_id))")

    except mariadb.Error as e:
        print(f"Error: {e}")


def connect(parameters: Dict[str, Union[str, int]]):
    try:
        # Establish a connection
        connection = mariadb.connect(**parameters)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = connection.cursor()
    print("connection opened")
    return connection, cur


def write_db(cursor):
    # insert information
    # example of correct request :
    # INSERT INTO `rpi` (`rpi_id`, `latitude`, `longitude`) VALUES ('2', '52.1168517', '2.6652337');
    now = datetime.datetime.now()
    print("now is ", now)
    try:
        cursor.execute("INSERT INTO rpi (rpi_id, latitude, longitude) VALUES (?, ?, ?)",
                       ('3', '1.0', '-1.0'))
        cursor.execute("INSERT INTO noises_levels (rpi_id, noise_level, datetime) VALUES (?, ?, ?)",
                       ('3', '2', f'{now}'))
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.commit()
    print(f"Last Inserted ID: {cursor.lastrowid}")


def read_db(cursor):
    cur = cursor
    # retrieving information
    rpi_id = 3
    cur.execute("SELECT latitude, longitude FROM rpi WHERE rpi_id=?", (rpi_id,))

    for latitude, longitude in cur:
        print(f"lat: {latitude}, long: {longitude}")


if __name__ == "__main__":
    # connection parameters
    conn_params = {
        "user": "user",
        "password": "password",
        "host": "127.0.0.1",
        "database": "soundfog",
        "port": 3306
    }
    conn, cur = connect(conn_params)
    # setup_database(cur)
    write_db(cur)
    read_db(cur)
    conn.close()
    print("connection closed")
