import sqlite3
from config import bot
import random


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot")
    cursor = db.cursor()
    if db:
        print("База данных подключена!")
    db.execute("CREATE TABLE IF NOT EXISTS menu"
               "(photo TEXT,name TEXT PRIMARY KEY , description TEXT, price TEXT)")

    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    r_m = random.randint(0, len(result) - 1)
    await bot.send_photo(message.from_user.id, result[r_m][0],
                         caption=f"Name: {result[r_m][1]}\n"
                                 f"Deskription: {result[r_m][2]}\n"
                                 f"Price: {result[r_m][3]}\n")
async def random_menu(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    r_m = random.randint(0, len(result) - 1)
    await bot.send_photo(message.chat.id, result[r_m][0])
    await bot.send_message(message.from_user.id,
                           f"Name: {result[r_m][1]}\n"
                           f"Deskription: {result[r_m][2]}\n"
                           f"Price: {result[r_m][3]}\n")
async def sql_command_all(message):
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(name):
    cursor.execute("DELETE FROM menu WHERE name == ?", (name,))
    db.commit()
