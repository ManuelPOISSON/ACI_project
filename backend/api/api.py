from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Any, Union
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


@app.post("/data")
def write_amplitude_in_db(raspberry_id: int, location_id: int, noise_amplitudes: List[List[Union[Any, float]]]):
    # print("parameters", raspberry_id, type(raspberry_id), noise_amplitudes, type(noise_amplitudes))
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    for date, noise_ampl in noise_amplitudes:
        print("write to database : ", date, noise_ampl)
        db_connector.write_amplitude(conn, cur, date, raspberry_id, location_id, noise_ampl)
    conn.close()
    return {
        "rasp_id": raspberry_id,
        "amplitudes": noise_amplitudes
    }


@app.get("/database")
def print_database():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    dump = db_connector.print_bd(cur)

    return {
        "database": dump
    }


@app.get("/write_fake_device")
def write_fake_device():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.write_fake_device(conn, cur)


@app.get("/write_fake_noise_level")
def write_fake_noise_level():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.write_fake_noise_level(conn, cur)


@app.delete("/delete_fake")
def delete_fake_data():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.delete_fake_data(conn, cur)

"""
# Add test data
@app.get("/add")
def add_map_data():
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.write_db(conn, cur)
    conn.close()
    return {"message": "done"}
"""
