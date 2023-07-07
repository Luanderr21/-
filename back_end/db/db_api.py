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
        operation = f"insert into video values('{vname}', null, null)"
        self.cursor.execute(operation)
        self.conn.commit()

    def addKey(self, vname, vkey):
        operation = f"update video set key = '{vkey}' where name = '{vname}'"
        self.cursor.execute(operation)
        self.conn.commit()

    def addResult(self, vkey, vresult):
        operation = f"update video set result = '{vresult}' where key = '{vkey}'"
        self.cursor.execute(operation)
        self.conn.commit()

    def getInfo(self, vname):
        operation = f"select * from video where name = '{vname}'"
        self.cursor.execute(operation)
        self.conn.commit()
        return self.cursor.fetchone()


    def close(self):
        self.conn.close()


