import requests
import sqlite3
import random
def get_setu():
    SQLPath = 'sql/setu.db'
    print(SQLPath)
    conn = sqlite3.connect(SQLPath)
    cursor = conn.cursor()
    cursor.execute("select img_base64 from my_setu where ID=?", (random.randint(1, 961),))
    base_64 = cursor.fetchone()[0].decode()

    return base_64
