#-*- coding:utf8 -*-
#coding=utf-8

import crawl
import time
import threading
import urllib2
from bs4 import BeautifulSoup

class crawl_Proxy(crawl.Crawl):
    def __init__(self):
        self.domestic_proxy_url = "http://www.haodailiip.com/guonei/"

    def crawl_proxy(self,max_pages=50000):
        pages = 1
        proxy_list = []
        whole_list = []
        while pages <= max_pages:
            url = self.domestic_proxy_url + str(pages)
            text = self.get_url_text(url)
            soup = BeautifulSoup(text,"html.parser")
            for proxy in soup.find_all("tr", {"style":"font-size: 16px;background-color:#F8F8FF;  line-height: 25px;"}):
                for ip in proxy.find_all("td"):
                    if "			" in ip.string:
                        a = ip.string.strip()
                        if len(proxy_list) < 2:
                            proxy_list.append(a)
                        else:
                            whole_list.append(proxy_list)
                            proxy_list = [a]
            for proxy in soup.find_all("tr", {"style":"font-size: 16px;line-height: 25px;"}):
                for ip in proxy.find_all("td"):
                    if "			" in ip.string:
                        a = ip.string.strip()
                        if len(proxy_list) < 2:
                            proxy_list.append(a)
                        else:
                            whole_list.append(proxy_list)
                            proxy_list = [a]
            pages += 1
            time.sleep(5)
        return whole_list

class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(proxy[0],proxy[1])})
            print proxy[0],proxy[1]
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t1 = time.time()
            try:
                checkedProxyList = []
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                if result != "" or None:
                    checkedProxyList.append((proxy[0],proxy[1],timeused))
                else:
                     continue
            except Exception,e:
                continue
        print checkedProxyList
        return checkedProxyList

    def run(self):
        self.checkProxy()

