import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect("Files.db")
    cur = base.cursor()
    base.commit()


async def sqlite_add_commads(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO file_v2 VALUES (?, ?, ?, ?, ?)',
                    tuple(data.values()))
        base.commit()


def sqlite_del_file(title):
    cur.execute('DELETE FROM file_v2 WHERE card_name = ?', (title,))
    base.commit()


def sqlite_add_category(name):
    cur.execute('INSERT INTO Categories(title) VALUES (?) ', (name,))
    base.commit()


def sqlite_del_category(name):
    cur.execute('DELETE FROM Categories WHERE title=?', (name,))
    cur.execute('DELETE FROM file_v2 WHERE ID=?', (name,))
    base.commit()


def get_all_user_id():
    cur.execute('SELECT user_id FROM users')
    data = cur.fetchall()
    return data
