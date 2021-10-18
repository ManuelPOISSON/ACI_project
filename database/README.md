# database structure

## rpi table                           
| rpi_id | latitude | longitude |
|--------|----------|-----------|
| 1      | 34       | 54        |
| 2      | 4        | 56        |
| 3      | 45       | 75        |

## noises_levels table
| rpi_id | noise    | time      |
|--------|----------|-----------|
| 1      | 5        | 12        |
| 1      | 4        | 13        |
| 1      | 5        | 14        |
| 1      | 4        | 15        |
| 1      | 5        | 16        |
| 1      | 4        | 13        |
| 2      | 1        | 12        |
| 2      | 2        | 13        |
| 2      | 5        | 14        |
| 2      | 4        | 15        |
| 2      | 7        | 16        |

it is a mariadb

# install python requirements
```bash
python3 -m venv name_of_env
source name_of_env/bin/activate
pip install -r requirements.txt  
```

# Usage
- lauch mariadb :
  - run `docker-compose up` or `sudo docker-compose up` if it didn't work
- modify and read data base : 
  - run `python db_connector.py`

 

## usefull links : 
- https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
- https://mariadb-corporation.github.io/mariadb-connector-python/usage.html