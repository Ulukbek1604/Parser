import sqlite3
from config import bot
import random

def sql_create():
    global db, cursor
    db = sqlite3.connect("bot_menu")
    cursor = db.cursor()
    if db:
        print("База данных подключена!")
    db.execute("CREATE TABLE IF NOT EXISTS anketa"
               "(id INTEGER PRIMARY KEY, nickname TEXT, photo TEXT, "
               "name TEXT, surname TEXT, age INTEGER, region TEXT)")
    db.commit()
async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES (?, ?, ?, ?)", tuple(data.values()))
        db.commit()