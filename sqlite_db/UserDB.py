import sqlite3
from client import DataBase
from sqlite_db import moneyDB as money

base = sqlite3.connect(DataBase)
cur = base.cursor()


def addUser(id, refer_id):
    if(refer_id != 0):
        money.add_referal(id, refer_id)
    cur.execute('INSERT INTO users (user_id, refer_id) VALUES (?, ?)',
                (id, refer_id))
    base.commit()


def Check_id(id, refer_id=0):
    cur.execute('SELECT * FROM users WHERE user_id =?', (id,))
    if(cur.fetchone() is None):
        addUser(id, refer_id)
    base.commit()


def bool_check_id(id):
    cur.execute('SELECT refer FROM users WHERE user_id =?', (id,))
    if(cur.fetchone() is None):
        return False
    return True


def write_last_category(id, last_category):
    cur.execute('UPDATE users SET last_category=? WHERE user_id=?',
                (last_category, id))
    base.commit()


def get_last_category(id):
    cur.execute('SELECT last_category FROM users WHERE user_id=?', (id,))
    data = cur.fetchone()
    for i in data:
        return i


def get_last_girl(id):
    cur.execute('SELECT last_girl FROM users WHERE user_id =?', (id,))
    for i in cur.fetchone():
        return i


def get_deckription(id):
    title = get_last_girl(id)
    cur.execute('SELECT description FROM file_v2 WHERE card_name=?', (title,))
    for i in cur.fetchone():
        return i
