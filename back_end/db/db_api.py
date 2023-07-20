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
        """
        插入视频
        :param vkey: 视频id
        :param vname: 视频文件名
        :return: None
        """
        operation = "insert into video values(?, ?, null, null, null)"
        self.cursor.execute(operation, (vkey, vname,))
        self.conn.commit()

    def addResult(self, vkey, vresult):
        """
        为视频添加识别结果
        :param vkey: 视频id
        :param vresult: 视频识别结果
        :return: None
        """
        operation = "update video set result = ? where key = ?"
        self.cursor.execute(operation, (vresult, vkey))
        self.conn.commit()

    def addReplacer(self, vkey, replacer_id):
        """
        为视频添加替换视频文件名
        :param vkey: 视频id
        :param replacer_id: 替换视频名
        :return: None
        """
        operation = "update video set replacer = ? where key = ?"
        self.cursor.execute(operation, (replacer_id, vkey, ))
        self.conn.commit()

    def addRepname(self, vkey, replaced_name):
        """
        为视频添加替换后文件名
        :param vkey: 视频id
        :param replaced_name: 替换后视频文件名
        :return: None
        """
        operation = "update video set rep_name = ? where key = ?"
        self.cursor.execute(operation, (replaced_name, vkey, ))
        self.conn.commit()

    def getVideo(self, vkey):
        """
        根据视频id获取唯一视频
        :param vkey: 视频id
        :return: 视频实体
        """
        operation = "select name from video where key = ?"
        self.cursor.execute(operation, (vkey,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def getResult(self, vkey):
        """
        根据视频id获取识别结果
        :param vkey: 视频id
        :return: 识别结果
        """
        operation = "select result from video where key = ?"
        self.cursor.execute(operation, (vkey,))
        self.conn.commit()
        vres = self.cursor.fetchone()
        return vres[0]


    def close(self):
        """
        关闭数据库
        :return: None
        """
        self.conn.close()
