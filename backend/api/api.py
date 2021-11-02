from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import datetime
import db_connector

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SoundFog API"}


@app.get("/map")
def read_map_data(start: Optional[datetime.datetime] = datetime.datetime.now() - datetime.timedelta(hours=1), end: Optional[datetime.datetime] = datetime.datetime.now()):
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.read_mean_values(cur, start, end)
    res = []
    for latitude, longitude, level in cur:
        res.append({"lat": latitude, "lng": longitude, "lvl": level})
    conn.close()
    return res

"""
# Add test data
@app.get("/add")
def add_map_data():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.write_db(conn, cur)
    conn.close()
    return {"message": "done"}
"""
