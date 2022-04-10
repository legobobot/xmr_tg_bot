import sqlite3


class Database:

    def get_keyboard(self):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            get_inline_key = """SELECT title FROM Categories"""
            cursor.execute(get_inline_key)
            data = cursor.fetchall()
            a = []
            for row in data:
                a.append(row)
        except sqlite3.Error as error:
            print("Error", error)
        finally:
            db.commit()
            return a

    @staticmethod
    def get_ID_Categories(title):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            get_id = f""" SELECT ID FROM Categories WHERE title = '{title}' """
            cursor.execute(get_id)
            data = cursor.fetchone()
            a = str(data[0])
        except sqlite3.Error as error:
            print("Error")
        finally:
            db.commit()
            return a

    @classmethod
    def girlkey(self, title):
        try:
            id = Database.get_ID_Categories(title)
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            get_girls_name = f"""SELECT arr_name FROM Files WHERE ID = '{id}' """
            cursor.execute(get_girls_name)
            data = (cursor.fetchall())
            a = []
            for row in data:
                a.append(row)
        except sqlite3.Error as error:
            print("Error")
        finally:
            db.commit()
            return a

    @staticmethod
    def get_images(preview_photos_id):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            get = f""" SELECT DISTINCT File_name, File, Description FROM  photos_prev WHERE preview_photos_id = '{preview_photos_id}' """
            cursor.execute(get)
            data = cursor.fetchall()
            for row in data:
                a = {'File_name': row[0],
                     'File': row[1], 'Description': row[2]}
        except sqlite3.Error as error:
            print("Error")
        finally:
            db.commit()
            return a

    @classmethod
    def getGirls_preview(self, title):
        try:
            db = sqlite3.connect("Files.db")
            cursor = db.cursor()
            get = f"""SELECT preview_photos_id FROM Files WHERE arr_name = '{title}' """
            cursor.execute(get)
            data = cursor.fetchall()
            a = Database.get_images(data[0][0])
        except sqlite3.Error as error:
            print("Error")
        finally:
            db.commit()
            return a
