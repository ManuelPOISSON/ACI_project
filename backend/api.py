from fastapi import FastAPI
from typing import Optional
import datetime
import db_connector

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SoundFog API"}


@app.get("/map")
def read_map_data(start: Optional[datetime.datetime] = datetime.datetime.now() - datetime.timedelta(hours=1), end: Optional[datetime.datetime] = datetime.datetime.now()):
    return {"start": start, "end": end}

@app.get("/add")
def add_map_data():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.write_db(conn, cur)
    conn.close()
    return {"message": "done"}
