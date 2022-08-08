import sqlite3
import logging

from sqlite3 import Cursor, Connection


logging.basicConfig(level=logging.INFO)


class DB:
    def __init__(self, dbname):
        self.connect: Connection = sqlite3.connect(dbname)
        self.cursor: Cursor = self.connect.cursor()

    def setup(self):
        setup_quert = '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL UNIQUE,
            user_name VARCHAR NOT NULL UNIQUE);'''
        self.connect.execute(setup_quert)
        self.connect.commit()

    def add_user_to_db(self, user_id, username):
        args = (user_id, username)
        self.connect.execute(
            '''INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?,?);''', args)
        self.connect.commit()

    def close(self):
        self.connect.close()
