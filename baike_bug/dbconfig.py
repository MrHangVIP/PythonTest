# coding:utf-8
import MySQLdb


class DB_Config(object):
    def connectDB(self):
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="zsxbishe")
        print conn
