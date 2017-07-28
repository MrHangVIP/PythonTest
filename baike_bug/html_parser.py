# coding:utf8
import re
import urlparse

from bs4 import BeautifulSoup

from baike_bug import html_downloader, db_util


class HtmlParser(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.dbutil = db_util.DB_Util()

    # 本地方法需要先定义在使用，也就是定义得放在前面不然无法调用
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.html 链接格式u.com/item/Guido%20van%20Rossum
        print 'link==>'
        links = soup.find_all('a', href=re.compile(r"/info/"))  # 找到所有的url，通过占位符表示数字
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

        # 文章数据解析

    def _parse_chapter(self, chapter_url):
        if chapter_url is None:
            return
        html_cont = self.downloader.download(chapter_url)
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        # new_urls = self._get_new_urls(chapter_url, soup)  # self调本地方法，通过url
        content_data = self._parse_content_data(chapter_url, soup)

        if content_data is not None:
            sql = "insert into t_content(chapterurl, content, nexturl, preurl) values " \
                  "('%s', '%s', '%s', '%s')" % \
                  (content_data['chapterUrl'], content_data['content'], content_data['nextUrl'],
                   content_data['preUrl'])
            self.dbutil.insert(sql)

        return None

    # < !--小说信息页面 -->
    #     < div class ="book-information cf" data-l1="2" >
    #     < div class ="book-img" >
    #     < a class ="J-getJumpUrl" id="bookImg" href="//read.qidian.com/chapter/7X3dt6Dj9tI1/frfuMcYFVZwex0RJOkJclQ2" data - eid = "qd_G09"data - bid = "3513193"data - firstchapterjumpurl = "" >
    #     < img src = "//qidian.qpic.cn/qdbimg/349573/3513193/180&#10;" > < / a > < / div >
    #     < div class ="book-info " >
    #  < h1 > < em > 雪鹰领主 < / em >
    # < span > < a class ="writer" href="//me.qidian.com/authorIndex.aspx?id=4362096" target="_blank" data-eid="qd_G08" > 我吃西红柿 < / a > 著 < / span > < / h1 >
    #     < p class ="intro" > 夏族的强者们征战四方，灭杀一切威胁！ < / p > 上万的就是带万字，不然直接是数字
    #     < p > < em > 360.12 < / em > < cite > 万字 < / cite > < i > | < / i > < em > 707.26 < / em > < cite > 万总点击 < span >· < / span > 会员周点击1686 < / cite > < i > | < / i > < em > 900.95 < / em > < cite > 万总推荐 < span >· < / span > 周8026 < / cite > < / p >
    #     < / div >
    #     < / div >
    # 图片，作者，点击量，总字数，是否完结，书名，简介
    def _parse_info_data(self, page_url, soup):  # 每次解析任意页面都应该抓取本页面的info url
        # self._get_new_urls(page_url, soup)
        info_data = {}
        if page_url.find("info") == -1:
            return
        info_data['info_url'] = page_url
        # 匹配title  <dd class="lemmaWgt-lemmaTitle-title">
        info_node = soup.find('div', class_="book-information cf")
        info_data['imageUrl'] = info_node.find('img').get('src')
        book_node = info_node.find('div', class_="book-info ")
        info_data['novelName'] = book_node.find('h1').get_text()
        info_data['author'] = book_node.find('h1').find('a', class_="writer").get_text()
        for p in book_node.find_all('p'):
            if p.get('class') is not None and str(p.get('class')).find("tag") != -1:
                # 解析span
                info_data['state'] = p.find('span').get_text()
                info_data['type'] = p.find('a').get_text()
                continue
            if p.get('class') is not None and str(p.get('class')).find("intro") != -1:  # 简介
                info_data['brief'] = p.get_text()
                continue
            if p.find_all('em') is not None:  # 字数和点击量
                i = 0;
                for em in p.find_all('em'):
                    if i == 0:  # 字数
                        info_data['wordsNum'] = em.get_text()
                    if i == 1:  # 点击量
                        info_data['clickNum'] = em.get_text()
                    i = i + 1

        return info_data

    # 章节信息解析 数据有：章节名称，章节url，章节数量，小说url
    def _parse_chapter_data(self, page_url, soup):
        chapter_list = []
        if page_url.find("info") == -1:
            return None
        count = 0
        # 匹配title  <dd class="lemmaWgt-lemmaTitle-title">
        chapter_list_node = soup.find('div', class_="volume-wrap")
        for chapter in chapter_list_node.find_all('li'):
            chapter_data = {}
            chapter_data['info_url'] = page_url
            chapter_data['chapterNum'] = count
            chapter_data['chapterName'] = chapter.get_text()
            chapter_data['chapterUrl'] = chapter.find('a').get('href')
            # join 方法会按照pageurl的格式将new_url补全
            chapter_data['chapterUrl'] = urlparse.urljoin(page_url, chapter_data['chapterUrl'])
            try:
                if chapter.find('a').get('href') is not None:
                    self._parse_chapter(chapter_data['chapterUrl'])  # 解析内容数据
            except:
                print "parse_chapter() fail "
            chapter_list.append(chapter_data)
        return chapter_data

    # 内容信息解析  文章内容，章节url，上一章节url，下一章节url
    def _parse_content_data(self, page_url, soup):
        # self._get_new_urls(page_url, soup)
        content_data = {}
        if page_url.find("chapter") == -1:
            return None
        content_data['chapterUrl'] = page_url
        content_node = soup.find('div', class_="read-content j_readContent")
        # content_data['content'] = content_node.get_text()
        content_data['content'] = "hahah"
        # p_nodes = content_node.find_all('p')
        # for content in p_nodes:
        #     content_data['content'] = content_data['content'] + '\\n' + content.get_text()

        content_data['nextUrl'] = ''
        content_data['preUrl'] = ''
        chapter_node = soup.find('div', class_="chapter-control dib-wrap")
        for a in chapter_node.find_all('a'):
            if a.get('id') is not None and a.get('id').find("j_chapterPrev") != -1:
                content_data['preUrl'] = a.get('href')
                continue
            if a.get('id') is not None and a.get('id').find("j_chapterNext") != -1:
                content_data['nextUrl'] = a.get('href')
                continue
        return content_data

    def parse(self, page_url):
        if page_url is None:
            return
        print page_url
        html_cont = self.downloader.download(page_url)
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)  # self调本地方法，通过url
        info_data = self._parse_info_data(page_url, soup)
        chapter_data = self._parse_chapter_data(page_url, soup)

        return new_urls, info_data, chapter_data


        # 逻辑 解析根url 找到该url 的所有 info url并且添加到集合。
        # 解析 下载这些info 页面 _parse_info_data解析其中的小说信息 _parse_chapter_data 解析其中的章节信息
        # 下载这些章节 页面 _parse_content_data解析具体的内容
