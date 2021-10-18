# Module Imports
import mariadb
import sys

# connection parameters
conn_params = {
    "user": "user",
    "password": "password",
    "host": "127.0.0.1",
    "database": "soundfog",
    "port": 3306
}

try:
    # Establish a connection
    conn = mariadb.connect(**conn_params)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
print("connection opened")

# retrieving information
rpi_id = 1
cur.execute("SELECT latitude, longitude FROM rpi WHERE rpi_id=?", (rpi_id,))

for latitude, longitude in cur:
    print(f"lat: {latitude}, long: {longitude}")

# insert information
# example of correct request :
# INSERT INTO `rpi` (`rpi_id`, `latitude`, `longitude`) VALUES ('2', '52.1168517', '2.6652337');
try:
    # cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria", "DB"))
    cur.execute("INSERT INTO rpi ('rpi_id', 'latitude', 'longitude') VALUES (?, ?, ?)",
                ('2', '52.2168517', '2.2652337'))
except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()
print(f"Last Inserted ID: {cur.lastrowid}")

conn.close()
