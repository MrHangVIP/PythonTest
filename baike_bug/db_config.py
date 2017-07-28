# coding:utf-8
import MySQLdb


class DB_Config(object):
    def connect(self):
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="noveldb", charset="utf8")
        return conn
