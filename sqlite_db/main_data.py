import sqlite3
from client import bot
import Keyboard as key

base = sqlite3.connect("Files.db")
cur = base.cursor()


def GET_GIRLS_INLINE_KEY(title):
    cur.execute('SELECT card_name FROM file_v2 WHERE ID=?', (title,))
    data_file = cur.fetchall()
    a = []
    for row in data_file:
        a.append(row)
    base.commit()
    return a


async def print_card(title, id):
    for row in cur.execute('SELECT DISTINCT preview_id, description FROM file_v2 WHERE card_name=?', (title,)):
        await bot.send_photo(id, photo=row[0], caption=row[1], reply_markup=key.buybtn)


def get_keyboard():
    get_inline_key = """SELECT title FROM Categories"""
    cur.execute(get_inline_key)
    return cur.fetchall()
