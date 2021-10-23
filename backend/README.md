# SoundFog backend

API and database for SoundFog project.

## Usage

- run `docker-compose up`
- API is accessible on http://localhost:8000

## Routes

### Public

| path | description |
|------|-------------|
| /    | API welcome message. Can be used to check if server is up |
| /map?start=\<datetime\>&end=\<datetime\> | Get data to display on the map |


## Database structure

### coordinates table

| id | current_coordinate |
|----|--------------------|
| 1  | 1                  |
| 2  | 2                  |
| 3  | 3                  |

### devices table

| id | latitude | longitude |
|----|----------|-----------|
| 1  | 34       | 54        |
| 2  | 4        | 56        |
| 3  | 45       | 75        |


### noise_levels table

| time                | device | coordinate | noise_level |
|---------------------|--------|------------|-------------|
| 2021-01-01 13:45:00 | 1      | 1          | 12        |
| 2021-01-01 13:45:15 | 1      | 1          | 13        |
| 2021-01-01 13:45:30 | 1      | 1          | 14        |
| 2021-10-20 22:10:00 | 1      | 3          | 15        |
| 2021-10-20 22:10:15 | 1      | 3          | 16        |
| 2021-10-20 22:10:30 | 1      | 3          | 13        |
| 2021-10-23 09:25:00 | 2      | 2          | 12        |
| 2021-10-23 09:25:15 | 2      | 2          | 13        |
| 2021-10-23 09:25:30 | 2      | 2          | 14        |
| 2021-10-23 09:25:45 | 2      | 2          | 15        |
| 2021-10-23 09:26:30 | 2      | 2          | 16        |


## Python scripts

### Install python requirements (no docker)

```bash
python3 -m venv name_of_env
source name_of_env/bin/activate
pip install -r requirements.txt  
```

### Usage

- lauch mariadb :
  - run `docker-compose up` or `sudo docker-compose up` if it didn't work
- modify and read data base : 
  - run `python db_connector.py`
 

### Usefull links : 
- https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
- https://mariadb-corporation.github.io/mariadb-connector-python/usage.html
