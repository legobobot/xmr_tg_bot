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
        print("Запись успешно добавлена в таблицу!")
        base.commit()


def sqlite_del_file(title):
    cur.execute('DELETE FROM file_v2 WHERE card_name = ?', (title,))
    print("Лот был успешно удален!")
    base.commit()
