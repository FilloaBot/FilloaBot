import sqlite3
from sqlite3 import Error
"""
def sql_connection():
    try:
        con = sqlite3.connect("database.db")
        return con
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE empleados(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")

def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE empleados SET name = "Rogers" where id = 2')
    con.commit()

con = sql_connection()
sql_update(con)
"""

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

#        for row in cursorObj.fetchall():
#           amount = row
        return cursorObj.fetchall()[0][0]

    def add_user_balance(self, user_name, balance):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name, balance,)

        cursorObj.execute("INSERT INTO balance VALUES(?, ?)", s)
        con.commit()

