# coding:utf8
import re, urllib2, bs4

from bs4 import BeautifulSoup

print bs4

# url = 'www.baidu,com'
#
# urllib2.urlopen(url, "", 100000)
#
# re.findall("")

html_doc = """ <div class="J-next-auto hide next-auto"><em>3</em> 秒后播放下一节</div>
                            <div class="J-next-btn hide next-auto btn btn-green">下一节</div>
                            <a href="/video/10687/0" class="review-course">重新观看</a>
                            
                            <div id="js-ques-box"></div>                        </div>

                                    </div>
"""
soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
print  '获取链接'
links = soup.find_all('a')
for link in links:
    print link.name, link['href'], link.get_text()

print '获取指定url'
link_node = soup.find('a', href='/video/10687/0')
print link_node.name, link_node['href'], link_node.get_text()

print '正则匹配'
link_node = soup.find('a', href=re.compile(r'video'))
print link_node.name, link_node['href'], link_node.get_text()

print '获取div'
link_node = soup.find('div', class_='J-next-auto hide next-auto')
print link_node.name, link_node.get_text()

print '获取div正则'
link_node = soup.find('div', id=re.compile(r'ques'))  # 正则可以模糊匹配
print link_node.name, link_node['id'], link_node.get_text()  # 如果匹配结果为空的时候输出会报错
