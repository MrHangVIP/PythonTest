# coding:utf8
class HtmlOutputer(object):
    def __init__(self):
        self.datas = [] #列表类型

    def collect_data(self, data):  # 收集数据
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):  # 将手机号的数据放到html
        fout = open("output.html","w") #文件的输出对象
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")  #表格形式
        #ascii
        for data in self.datas:
            fout.write("<tr>") #每行
            fout.write("<td>%s<td>" % data['url'])#单元内容
            fout.write("<td>%s<td>" % data['title'].encode('utf-8'))#防止输出乱码
            fout.write("<td>%s<td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")#闭合标签
        fout.write("</body>")
        fout.write("</html>")
        fout.close()