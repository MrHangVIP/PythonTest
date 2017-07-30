# coding:utf8
import os


class FileOutPut(object):
    def __init__(self):
        self.data = {}

    # 参数 文件数据，文件夹名称，文件名称
    def file_output(self, data, dirname, filename):
        filepath = r'../novelfile/%s/' % dirname
        if os.path.exists(filepath) is False:
            os.mkdir(filepath)
        try:
            filehandle = open(filepath + filename + ".txt", "w")
            filehandle.write(data.encode("utf-8"))
            filehandle.close()
        except Exception, e:
            print e
        return filepath + filename + ".txt"
