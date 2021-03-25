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
            # print("El usuario no existe melon")
            return None

        return int(out[0][0])

    def get_user_bank(self, user_name):
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
        s = (user_name, )
        cursorObj.execute("SELECT bank FROM balance WHERE user = ?", s)

        out = cursorObj.fetchall()

        if not out:
            return None
        
        return int(out[0][0])

    def add_user_balance(self, user_name, balance = 0):
        current_balance = self.get_user_balance(user_name)
        if current_balance == None:
            current_balance = 0
        balance = current_balance + balance
        if balance < 0:
            return None
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()

        if not self.user_exist(user_name):
            s = (user_name, balance, 0, )
            cursorObj.execute("INSERT INTO balance VALUES(?, ?, ?)", s)

        else:
            s = (balance, user_name,)
            cursorObj.execute("UPDATE balance SET amount = ? WHERE user = ?", s)

        con.commit()
        return balance
        
    def substract_balance(self, user_name, balance = 0):
        current_balance = self.get_user_balance(user_name)
        if current_balance == None:
            # print(f"{user_name} has no money in his account")
            return None

        substract_balance = balance
        current_balance = current_balance - substract_balance
        if current_balance < 0:
            return None
        
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()

        if self.user_exist(user_name):
            s = (current_balance, user_name, )
            cursorObj.execute("UPDATE balance SET amount = ? WHERE user = ?", s)
        else:
            # print(f"User {user_name} does not exist")
            return None

        con.commit()
        return current_balance

    def deposit(self, user_name, balance: int):   
        current_bank_balance = self.get_user_bank(user_name)
        current_bank_balance += balance

        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()

        s = (current_bank_balance, user_name, )
        cursorObj.execute("UPDATE balance SET bank = ? WHERE user = ?", s)
        con.commit()

        self.substract_balance(user_name, balance)

        return balance

    def withdraw(self, user_name, balance: int):
        current_balance = self.get_user_bank(user_name)

        current_balance -= balance
        
        con = sqlite3.connect(self.database)
        cursorObj = con.cursor()
    
        s = (current_balance, user_name, )
        cursorObj.execute("UPDATE balance SET bank = ? WHERE user = ?", s)
        con.commit()

        self.add_user_balance(user_name, balance)
        
        return current_balance

    def exchange_balance(self, fromUser, targetUser, amount):
        fromUserBalance = self.substract_balance(fromUser, amount)
        targetUserbalance = self.add_user_balance(targetUser, amount)
        if fromUserBalance == None or targetUserbalance == None:
            return None
        out ={
            "from_user_balance": fromUserBalance,
            "target_user_balance": targetUserbalance
        }
        return out

    """
    Music operations in the dabase. A pechi le gusta oliveira
    """
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
            loopPos = out[3]
            loopPos -= 1
        data = {
            "guildId": out[0],
            "queue": out[1].split(";;;"),
            "loop": bool(out[2]),
            "loopPos": loopPos,
            "shuffle": bool(out[4]),
            "currentPos": out[5] or 0
        }

        return data
    def modify_queue(self, guildId, queue=None, loop=None, loopPos=None, shuffle=None, currentPos=None):
        if queue == None:
            if self.get_queue(guildId) == None:
                queue = None
            else:
                queue = self.get_queue(guildId)["queue"]
                queue = ";;;".join(queue)
        else:
            queue = ";;;".join(queue)
        if loop == None:
            if self.get_queue(guildId) == None:
                loop = False
            else:
                loop = self.get_queue(guildId)["loop"]
        if shuffle == None:
            if self.get_queue(guildId) == None:
                shuffle = False
            else:
                shuffle = self.get_queue(guildId)["shuffle"]
        if loopPos == None:
            if self.get_queue(guildId) == None:
                loopPos = 0
            else:
                loopPos = self.get_queue(guildId)["loopPos"]
                if loopPos == None:
                    loopPos=0
                else:
                    loopPos+=1
        else:
            loopPos += 1
        if currentPos == None:
            if self.get_queue(guildId) == None:
                currentPos = 0
            else:
                currentPos = self.get_queue(guildId)["currentPos"]
        

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
        return currentPos

    
