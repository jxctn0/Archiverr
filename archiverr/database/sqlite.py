import sqlite3


class SQLiteDatabase:
    def __init__(self, path="warehouse.db"):
        self.path = path

    def connect(self):
        return sqlite3.connect(self.path)
