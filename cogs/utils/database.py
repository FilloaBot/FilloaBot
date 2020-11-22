import sqlite3
from sqlite3 import Error

class main_db():
    def __init__(self, database):
        self.database = database

    def user_exist(self, user_name):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name,)
        cursorObj.execute("SELECT user FROM balance WHERE user = ?", s)

        return (cursorObj.fetchall().len() == 0)
    
    def get_user_balance(self, user_name):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name,)
        cursorObj.execute("SELECT amount FROM balance WHERE user = ?", s)

        if not cursorObj.fetchall():
            print("El usuario no existe melon")
            return None

        return cursorObj.fetchall()

    def add_user_balance(self, user_name, balance = 0):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name, balance,)

        cursorObj.execute("INSERT INTO balance VALUES(?, ?)", s)
        con.commit()

