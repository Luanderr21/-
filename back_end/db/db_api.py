import os.path
import sqlite3


class DataBase(object):
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.abspath(__file__), "../database.db"))
        self.cursor = self.conn.cursor()

    def createTable(self):
        self.cursor.execute("create table if not exists video("
                            "key text primary key not null, "
                            "name text, "
                            "result text, "
                            "rep_name text, "
                            "replacer text"
                            ")")
        self.conn.commit()

    def newVideo(self, vkey, vname):
        operation = "insert into video values(?, ?, null, null, null)"
        self.cursor.execute(operation, (vkey, vname,))
        self.conn.commit()

    def addResult(self, vkey, vresult):
        operation = "update video set result = ? where key = ?"
        self.cursor.execute(operation, (vresult, vkey))
        self.conn.commit()

    def addReplacer(self, vkey, replacer_id):
        operation = "update video set replacer = ? where key = ?"
        self.cursor.execute(operation, (replacer_id, vkey, ))
        self.conn.commit()

    def addRepname(self, vkey, replaced_name):
        operation = "update video set rep_name = ? where key = ?"
        self.cursor.execute(operation, (replaced_name, vkey, ))
        self.conn.commit()

    def getVideo(self, vkey):
        operation = "select name from video where key = ?"
        self.cursor.execute(operation, (vkey,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def getResult(self, vkey):
        operation = "select result from video where key = ?"
        self.cursor.execute(operation, (vkey,))
        self.conn.commit()
        vres = self.cursor.fetchone()
        return vres[0]


    def getReps(self, vkey):
        operation = "select "


    def close(self):
        self.conn.close()
