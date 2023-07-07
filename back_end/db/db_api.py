import os.path
import sqlite3


class DataBase(object):
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.abspath(__file__), "../database.db"))
        self.cursor = self.conn.cursor()

    def createTable(self):
        self.cursor.execute("create table if not exists video("
                            "name int primary key not null, "
                            "result text, "
                            "key text"
                            ")")
        self.conn.commit()

    def newVideo(self, vname):
        operation = "insert into video values(?, null, null)"
        params = [vname]
        self.cursor.execute(operation, params)
        self.conn.commit()

    def addKey(self, vname, vkey):
        operation = "update video set key = ? where name = ?"
        params = [vname, vkey]
        self.cursor.execute(operation, params)
        self.conn.commit()

    def addResult(self, vkey, vresult):
        operation = f"update video set result = ? where key = ?"
        params = [vresult, vkey]
        self.cursor.execute(operation, params)
        self.conn.commit()

    def getInfo(self, vname):
        operation = f"select * from video where name = ?"
        params = [vname]
        self.cursor.execute(operation, params)
        self.conn.commit()
        return self.cursor.fetchone()


    def close(self):
        self.conn.close()


