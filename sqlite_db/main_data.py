import sqlite3
from client import bot
import Keyboard as key
from client import DataBase

base = sqlite3.connect(DataBase)
cur = base.cursor()


def GET_GIRLS_INLINE_KEY(title):
    cur.execute('SELECT card_name FROM file_v2 WHERE ID=?', (title,))
    data_file = cur.fetchall()
    a = []
    for row in data_file:
        a.append(row)
    base.commit()
    return a


def write_last_girl(last_girl, id):
    try:
        cur.execute('UPDATE users SET last_girl=? WHERE user_id=?',
                    (last_girl, id))
    except sqlite3.Error as err:
        print("sqlite Error: ", err)
    finally:
        base.commit()


async def print_card(title, id):
    write_last_girl(title, id)
    for row in cur.execute('SELECT DISTINCT preview_id, description FROM file_v2 WHERE card_name=?', (title,)):
        await bot.send_photo(id, photo=row[0], caption=row[1], reply_markup=key.buybtn)


def get_keyboard():
    get_inline_key = """SELECT title FROM Categories"""
    cur.execute(get_inline_key)
    return cur.fetchall()
