import sqlite3
import random
import os
def on_connect():
    SQLPath = 'sql/BotSQL.db'
    # print(SQLPath)
    conn = sqlite3.connect(SQLPath)
    cursor = conn.cursor()

    return cursor


def get_morning():
    c = on_connect()
    c.execute("select text from morning where ID=?", (random.randint(1, 117),))
    text = c.fetchone()
    return text[0]


def get_netease():
    c = on_connect()
    c.execute("select * from netease where ID=?", (random.randint(1, 25),))
    text = c.fetchone()
    return text[1]


def get_token():
    c = on_connect()
    c.execute("select * from BaiduApi order by id desc limit 0,1")
    return c.fetchone()

def refresh_token(data):
    c = on_connect()
    c.execute("INSERT INTO BaiduApi\(\"access_token\", \"get_time\"\) VALUES (?,?)",(data['access_token'], data['get_token_time']))
    return


if __name__ == '__main__':
    print(get_netease())

