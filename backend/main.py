import db_connector
import uvicorn

if __name__ == "__main__":
    conn, cur = db_connector.connect(db_connector.connection_parameters)
    db_connector.setup_database(cur)
    conn.close()
    print("Start uvicorn server", flush=True)
    uvicorn.run("api:app", host="0.0.0.0", port=8000, access_log=True)
