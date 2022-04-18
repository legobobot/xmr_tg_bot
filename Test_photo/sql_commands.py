import sqlite3

base = sqlite3.connect("Files.db")
cur = base.cursor()


def max_s_photo():
    cur.execute('SELECT MAX(ID) FROM test_data')
    return cur.fetchone()[0]


def get_user_try_number(id):
    cur.execute('SELECT test_photo_try FROM users WHERE user_id=?', (id,))
    return cur.fetchone()[0]


def plus_try_photo(id):
    x = get_user_try_number(id)+1
    cur.execute(
        'UPDATE users SET test_photo_try=? WHERE user_id=?', (x, id))
    base.commit()


def get_one(id):
    users_number = get_user_try_number(id)
    cur.execute('SELECT image_id FROM test_data WHERE ID=?', (users_number,))
    data = cur.fetchone()
    plus_try_photo(id)
    return data[0]


def get_all_file():
    cur.execute('SELECT ID FROM test_data')
    return cur.fetchall()


def send_file_prev(ID):
    cur.execute('SELECT image_id FROM test_data WHERE ID=?', (ID,))
    return cur.fetchone()


def add_file(file_id):
    try:
        cur.execute('INSERT INTO test_data(image_id) VALUES(?)', (file_id, ))
    except:
        print(3482)
    finally:
        base.commit()


def del_file(image_id):
    cur.execute('DELETE FROM test_data WHERE image_id=?', (image_id,))
    base.commit()
