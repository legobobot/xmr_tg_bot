import sqlite3


base = sqlite3.connect("Files.db")
cur = base.cursor()


def addUser(id):
    cur.execute('INSERT INTO users (user_id) VALUES (?)', (id,))
    base.commit()


def Check_id(id):
    cur.execute('SELECT * FROM users WHERE user_id =?', (id,))
    if(cur.fetchone() is None):
        addUser(id)
    base.commit()


def write_last_category(id, last_category):
    cur.execute('UPDATE users SET last_category=? WHERE user_id=?',
                (last_category, id))
    base.commit()


def get_last_category(id):
    cur.execute('SELECT last_category FROM users WHERE user_id=?', (id,))
    data = cur.fetchone()
    for i in data:
        return i
