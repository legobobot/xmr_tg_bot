import sqlite3


class Users:

    @staticmethod
    def addUser(id):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (id,))
        except sqlite3.Error as error:
            print("sqlite Error", error)
        finally:
            print("пользователь был добавлен успешно!")
            db.commit()

    @classmethod
    def Check_id(self, id):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            info = cursor.execute(
                'SELECT * FROM users WHERE user_id =?', (id,))
            if(info.fetchone() is None):
                print("users not found")
                Users.addUser(id)
            else:
                print("user is true")
        except sqlite3.Error as error:
            print("sqlite Error", error)
        finally:
            db.commit()
