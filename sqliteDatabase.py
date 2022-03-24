import sqlite3
from sqlite3 import Error
from dataclasses import dataclass


@dataclass
class ApiResponse:
    api: str
    code: int
    msg: str
    timestamp: int


def init_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("DROP TABLE IF EXISTS LAST_STATUS;")

        conn.execute('''CREATE TABLE IF NOT EXISTS LAST_STATUS
                     (API     CHAR(100)          NOT NULL,
                     CODE            INT     NOT NULL,
                     LAST_RESPONSE        CHAR(100),
                     TIMESTAMP            INT     NOT NULL);''')

        conn.commit()
        print(f"Successfully initialized sqlite db: {sqlite3.version}")
    except Error as e:
        print(f"Error initializing sqlite: {e}")
    finally:
        if conn:
            conn.close()


def update_db(api: str, code: int, msg: str, timestamp: int):
    conn = sqlite3.connect(r"/pyScript/nova.db")
    conn.execute(
        f"""INSERT OR IGNORE INTO LAST_STATUS (API,CODE,LAST_RESPONSE,TIMESTAMP) VALUES (\'{api}\', {code}, \'{msg}\', {timestamp})""")
    conn.execute(
        f"UPDATE LAST_STATUS SET LAST_RESPONSE=\'{msg}\', CODE = {code}, TIMESTAMP = {timestamp} WHERE API=\'{api}\'; ")

    conn.commit()
    conn.close()


def get_from_db():
    dynuResp = None
    ipfyResp = None
    conn = sqlite3.connect(r"/pyScript/nova.db")
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM LAST_STATUS;""")
    records = cur.fetchall()
    for row in records[0:2]:
        if row[0] == "dynu":
            dynuResp = ApiResponse(api=row[0], code=row[1], msg=row[2], timestamp=row[3])
        else:
            ipfyResp = ApiResponse(api=row[0], code=row[1], msg=row[2], timestamp=row[3])

    conn.close()

    return dynuResp, ipfyResp
