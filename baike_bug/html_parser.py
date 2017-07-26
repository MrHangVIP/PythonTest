# coding:utf8
import re
import urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):

    #本地方法需要先定义在使用，也就是定义得放在前面不然无法调用
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.html 链接格式u.com/item/Guido%20van%20Rossum
        print 'link==>'
        links = soup.find_all('a', href=re.compile(r"/item/"))  # 找到所有的url，通过占位符表示数字
        for link in links:
            print link
            new_url = link['href']
            # join 方法会按照pageurl的格式将new_url补全
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

            # 解析数据

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url
        # 匹配title  <dd class="lemmaWgt-lemmaTitle-title">
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find()
        res_data['title'] = title_node.get_text()
        # 匹配描述  <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)  # self调本地方法，通过url
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
