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
        self.cursor.execute(operation, (vname, ))
        self.conn.commit()

    def addKey(self, vname, vkey):
        operation = "update video set key = ? where name = ?"
        self.cursor.execute(operation, (vkey, vname))
        self.conn.commit()

    def addResult(self, vkey, vresult):
        operation = "update video set result = ? where key = ?"
        self.cursor.execute(operation, (vresult, vkey))
        self.conn.commit()

    def getInfo(self, vname):
        operation = "select * from video where name = ?"
        self.cursor.execute(operation, (vname, ))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def getResult(self, vkey):
        operation = "select result from video where key = ?"
        self.cursor.execute(operation, (vkey, ))
        self.conn.commit()
        vres = self.cursor.fetchone()
        return vres[0]

    def close(self):
        self.conn.close()


