# -*- coding: utf-8 -*-


import src.caesar
import sqlite3



class SQLManage:
    def __init__(self, basedate):
        self.db = sqlite3.connect(basedate, check_same_thread=False)
        self.cursor = self.db.cursor()
        with self.db:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS data (
	name TEXT NOT NULL,
	login TEXT NOT NULL,
	password TEXT NOT NULL,
        logpass TEXT NOT NULL)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS password (
        pass TEXT NOT NULL)''')

    def add_password(self, password):
        password_crypt = src.caesar.crypt(password, 5)
        with self.db:
            return self.cursor.execute(f'INSERT INTO password (pass) VALUES ("{password_crypt}")').fetchall()

    def check_password(self):
        with self.db:
            password = self.cursor.execute(
                'SELECT pass FROM password').fetchall()
            if password == []:
                return False
            else:
                return src.caesar.decrypt(password[0][0], 5)

    def add_data(self, name, login, password):
        password = src.caesar.crypt(password, 3)
        logpass = f"{name} ---> {login}:{password}"
        with self.db:
            return self.cursor.execute(f"INSERT INTO data (name, login, password, logpass) VALUES (?, ?, ?, ?)", (name, login, password, logpass)).fetchall()

    def check_name(self, name):
        with self.db:
            data = self.cursor.execute(f'SELECT login FROM data WHERE name = "{name}"').fetchall()
            if data == []:
                return True
            return False

    def get_all(self):
        with self.db:
            return self.cursor.execute("SELECT name FROM data").fetchall()

    def get_byname(self, name):
        with self.db:
            return self.cursor.execute(f'SELECT * FROM data WHERE name = "{name}"').fetchall()

    def delete_data(self, name):
        with self.db:
            return self.cursor.execute(f'DELETE FROM data WHERE name = "{name}"').fetchall()

    def delete_all(self):
        with self.db:
            return self.cursor.execute('DELETE FROM data').fetchall()

    def update_password(self, password):
        password = src.caesar.crypt(password, 5)
        with self.db:
            return self.cursor.execute(f'UPDATE password SET pass = "{password}"').fetchall()
