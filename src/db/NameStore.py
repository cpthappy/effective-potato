import sqlite3

DB_PATH = "names.db"

class NameStore(object):

    def __init__(self):
        self.db_path = DB_PATH
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def get_entry_by_name(self, name):
        try:
            self.cursor.execute("SELECT * FROM NAMES WHERE NAME=?", [(name)])
            data = self.cursor.fetchall()

            return data
        except sqlite3.Error:
            pass

    def get_unrated_entries(self):
        try:
            self.cursor.execute("SELECT * FROM NAMES WHERE RATING<0")
            data = self.cursor.fetchall()

            return data
        except sqlite3.Error:
            pass

if __name__ == "__main__":
    name_store = NameStore()
    print name_store.get_unrated_entries()
    print name_store.get_entry_by_name("Lara")
