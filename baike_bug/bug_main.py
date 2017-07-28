# coding:utf8
from baike_bug import url_manager, html_downloader, html_parser, html_output, db_config, db_util


class BugMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_output.HtmlOutputer()
        self.dbutil = db_util.DB_Util()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                new_urls, info_data, chapter_datas = self.parser.parse(new_url)
                self.urls.add_new_urls(new_urls)
                # 存储数据到数据库中
                if info_data is not None:
                    sql = "insert into t_novel(novelurl, novelname, clicknum, wordsnum, type, " \
                          "author, isfinish, biref, imageurl) values " \
                          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %\
                          (info_data['info_url'] ,info_data['novelName'], info_data['clickNum'],
                           info_data['wordsNum'], info_data['type'], info_data['author'], info_data['state'],
                           info_data['brief'], info_data['imageUrl'])
                    self.dbutil.insert(sql)

                if chapter_datas is not None:
                    for chapter_data in chapter_datas:
                        sql = "insert into t_chapter(novelurl, chaptername, chapterurl, chapternum) values " \
                              "('%s', '%s', '%s', '%s')" % \
                              (chapter_data['info_url'], chapter_data['chapterName'], chapter_data['chapterUrl'],
                               chapter_data['chapterNum'])
                        self.dbutil.insert(sql)
                # if count == 2:
                #     break
                count = count + 1
            except:
                print 'craw fail'
        print 'finish'
        # 关闭数据库连接
        self.dbutil.close()
            # self.outputer.output_html()
        self.dbutil.db.close()#关闭数据库链接


if __name__ == "__main__":
    root_url = "http://www.qidian.com/"
    ojb_bug = BugMain()
    ojb_bug.craw(root_url)
