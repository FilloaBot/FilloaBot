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

        con.commit()
        return not (len(cursorObj.fetchall()) == 0)
    
    def get_user_balance(self, user_name):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name,)
        cursorObj.execute("SELECT amount FROM balance WHERE user = ?", s)

        if not cursorObj.fetchall():
            print("El usuario no existe melon")
            
            con.commit()
            return None

        con.commit()
        return cursorObj.fetchall()  

    def add_user_balance(self, user_name, balance = 0):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name, balance,)
        
        if self.user_exist(user_name):
            cursorObj.execute("INSERT INTO balance VALUES(?, ?)", s)
        
        else:
            s = (balance, user_name,)
            cursorObj.execute("UPDATE balance SET amount = ? WHERE user = ?", s)

        con.commit()