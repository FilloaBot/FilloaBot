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

        out = cursorObj.fetchall()

        if not out:
            print("El usuario no existe melon")
            return None

        return out[0][0]

    def add_user_balance(self, user_name, balance = 0):
        current_balance = self.get_user_balance(user_name)
        if current_balance == None:
            current_balance = 0
        balance = current_balance + balance

        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name, balance,)

        if not self.user_exist(user_name):
            cursorObj.execute("INSERT INTO balance VALUES(?, ?)", s)

        else:
            s = (balance, user_name,)
            cursorObj.execute("UPDATE balance SET amount = ? WHERE user = ?", s)

        con.commit()

    ## Starts part for the music cog
    def queue_exist(self, guildId):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (guildId,)
        cursorObj.execute("SELECT guildId FROM musicQueues WHERE guildId = ?", s)

        con.commit()
        return not (len(cursorObj.fetchall()) == 0)

    def get_queue(self, guildId):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        if not self.queue_exist(guildId):
            return None
        s = (guildId,)

        cursorObj.execute("SELECT * FROM musicQueues WHERE guildId = ?", s)
        out = cursorObj.fetchall()[0]
        if out[3] == 0:
            loopPos = None
        else:
            loopPos -= 1
        data = {
            "guildId": out[0],
            "queue": out[1].split(";;;"),
            "loop": bool(out[2]),
            "loopPos": out[3],
            "shuffle": bool(out[4]),
            "currentPos": out[5] or 0
        }

        return data
    def modify_queue(self, guildId, queue=None, loop=False, loopPos=None, shuffle=False, currentPos=None):
        if loopPos == None:
            loopPos = 0
        if queue == None:
            if self.get_queue(guildId) == None:
                queue = None
            else:
                queue = self.get_queue(guildId)["queue"]

        queue = ";;;".join(queue)
        loop = int(loop)
        shuffle = int(shuffle)

        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()

        if self.queue_exist(guildId):
            s = (queue, loop, loopPos, shuffle, currentPos, guildId,)
            cursorObj.execute("UPDATE musicQueues SET queue = ?, loop = ?, loopPos = ?, shuffle = ?, currentPos = ? WHERE guildId = ?", s)
        else:
            s = (guildId, queue, loop, loopPos, shuffle, currentPos,)
            cursorObj.execute("INSERT INTO musicQueues VALUES(?,?,?,?,?,?)", s)
        con.commit()

    def insert_into_queue(self, guildId, ytId):
        queue = self.get_queue(guildId)
        if queue == None:
            queue = []
        else:
            queue = queue["queue"]
        queue.append(ytId)
        self.modify_queue(guildId, queue=queue)
        return queue
    
    def remove_from_queue(self, guildId, delPos):
        queue = self.get_queue(guildId)
        if queue == None:
            queue = []
        else:
            queue = queue["queue"]
        del queue[delPos]
        self.modify_queue(guildId, queue=queue)
        return queue

    def clear_queue(self, guildId):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()

        s = (guildId,)
        cursorObj.execute("DELETE FROM musicQueues WHERE guildId = ?", s)
        
        con.commit()

    def increment_current_pos(self, guildId):
        queue = self.get_queue(guildId)
        if queue == None:
            currentPos = -1
        else:
            currentPos = queue["currentPos"]
            currentPos += 1
            if currentPos >= len(queue["queue"]):
                currentPos = 0
        self.modify_queue(guildId, currentPos=currentPos)
        return currentPos

    def decrement_current_pos(self, guildId):
        queue = self.get_queue(guildId)
        if queue == None:
            currentPos = -1
        else:
            currentPos = queue["currentPos"]
            currentPos -= 1
            if currentPos < 0:
                currentPos = len(queue["queue"]) -1
        self.modify_queue(guildId, currentPos=currentPos)
        print(currentPos)
        return currentPos

    