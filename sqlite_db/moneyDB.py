import sqlite3
from sqlite_db import UserDB as user
from client import DataBase

base = sqlite3.connect(DataBase)
cur = base.cursor()

# get_commands-------


def get_balans(id):
    cur.execute('SELECT money FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i


def get_all_money(id):
    cur.execute('SELECT all_money FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i


def get_purchased(id):
    cur.execute('SELECT purchased FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i
# -------------------------


def get_referal(id):
    cur.execute('SELECT refer FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i


def add_referal(id_user, id_dad):
    if(user.bool_check_id(id_user) == False):
        cur.execute('UPDATE users SET refer=? WHERE user_id=?',
                    (get_referal(id_dad)+1, id_dad))
        base.commit()


def is_refer(id):
    cur.execute('SELECT refer_id FROM users WHERE user_id=?', (id,))
    return True if cur.fetchone()[0] != None else False


def get_my_referal(id):
    cur.execute('SELECT refer_id FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i


def add_refer_money(id, money):
    money_dad = cur.execute(
        'SELECT refer_money FROM users WHERE user_id=?', (id,)).fetchone()[0]
    cur.execute('UPDATE users SET refer_money=? WHERE user_id=?',
                (money + money_dad, id))
    base.commit()


def add_money_to_referal(id, money):
    if(is_refer(id)):
        refer = get_my_referal(id)
        cur.execute('UPDATE users SET money=? WHERE user_id=?',
                    ((money) + get_balans(refer), refer))
        base.commit()
        add_refer_money(refer, money)


def get_money_via_refer(id):
    cur.execute('SELECT refer_money FROM users WHERE user_id=?', (id,))
    for i in cur.fetchone():
        return i

# -----------------------------


def add_purchased(id):
    cur.execute('UPDATE users SET purchased=? WHERE user_id=?',
                (get_purchased(id)+1, id))
    base.commit()


def add_allmoney(id, money):
    cur.execute('UPDATE users SET all_money=? WHERE user_id=?',
                (get_all_money(id) + money, id))
    base.commit()


def add_money(id, money):
    cur.execute('UPDATE users SET money=? WHERE user_id=?',
                (get_balans(id) + money, id))
    base.commit()
    add_money_to_referal(id, money)
    add_allmoney(id, money)


def minus_money(id, money):
    cur.execute('UPDATE users SET money=? WHERE user_id=?',
                (get_balans(id) - money, id))
    base.commit()

# ------------------------------------------


def get_file(id):
    cur.execute('SELECT file_id FROM file_v2 WHERE card_name=?',
                (user.get_last_girl(id),))
    for i in cur.fetchone():
        return i

# ----------------------------------------------------


def add_payments_par(user_id=None, money=None, bill_id=None):
    cur.execute('INSERT INTO buy (user_id, money, bill_id) VALUES (?, ?, ?)',
                (user_id, money, bill_id,))
    base.commit()


def get_payments_par(bill_id):
    result = cur.execute(
        'SELECT * FROM buy WHERE bill_id =?', (bill_id)).fetchmany(1)
    return False if not bool(len(result)) else result


def get_added_money(user_id):
    cur.execute('SELECT money FROM buy WHERE user_id=?', (user_id,))
    for i in cur.fetchone():
        return i


def delete_bill_id(bill_id):
    cur.execute('DELETE FROM buy WHERE bill_id=?', (bill_id,))
    base.commit()
