# coding:utf-8
import MySQLdb


class DB_Config(object):
    def connect(self):
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="12345", db="noveldb", charset="utf8")
        return conn
