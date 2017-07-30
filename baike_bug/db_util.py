# encoding:utf8
import sys

from baike_bug import db_config

defaultencoding = 'utf-8'


class DB_Util(object):
    def __init__(self):
        if sys.getdefaultencoding() != defaultencoding:
            reload(sys)
            sys.setdefaultencoding(defaultencoding)
        self.db = db_config.DB_Config().connect()
        self.cursor = self.db.cursor()

    def insert(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception, e:
            # 发生错误时回滚
            print "insert fail:" + e
            self.db.rollback()

    def query(self, sql):
        # fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
        # fetchall():接收全部的返回结果行.
        # rowcount: 这是一个只读属性，并返回执行execute()
        # 方法后影响的行数。
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                fname = row[0]
                lname = row[1]
                age = row[2]
                sex = row[3]
                income = row[4]
                # 打印结果
                print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                      (fname, lname, age, sex, income)
        except:
            print "Error: unable to fecth data"
