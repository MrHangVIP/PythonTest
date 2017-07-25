# coding:utf8
import urllib2


class HtmlDownloader(object):
    def download(self, url):  # 要下载的url
        if url is None:
            return None
        response = urllib2.urlopen(url)
        if response.getode() != 200:
            return None

        return response.read()
