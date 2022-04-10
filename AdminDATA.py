import sqlite3


class Admin:
    def add_file(self, file):
        try:
            db = sqlite3.connect("File.db")
            cursor = db.cursor()
            cursor.execute('INSERT INTO ', (file))
        except sqlite3.Error as error:
            print("Error in sqlite3", error)
        finally:
            print("Файл был успешно добавлен!")
            db.commin()

    def del_file(self):
        pass

    def add_cat(self):
        pass

    def del_cat(self):
        pass
