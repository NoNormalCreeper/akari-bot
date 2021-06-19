import base64
import os
import re
import sqlite3
import traceback

dbpath = os.path.abspath('./modules/weekly_rss/save.db')


class MD:
    def __init__(self):
        if not os.path.exists(dbpath):
            self.initialize()

        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor()

    def initialize(self):
        a = open(dbpath, 'w')
        a.close()
        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE weekly
               (TITLE TEXT PRIMARY KEY     NOT NULL,
               LINK TEXT,
               PDESC TEXT,
               IMAGE TEXT,
               PDATE TEXT);''')

        self.c.close()


    def add_news(self, title, link, desc, image, date):
        self.c.execute(f"INSERT INTO weekly (TITLE, LINK, PDESC, IMAGE, PDATE) VALUES (?, ?, ?, ?, ?)", (title, link, desc, image, date))
        self.conn.commit()
        return

    def check_exist(self, title):
        a = self.c.execute(f"SELECT * FROM weekly WHERE TITLE=?", (title,)).fetchone()
        if a:
            return True
        else:
            return False
