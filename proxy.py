#-*- coding:utf8 -*-
#coding=utf-8

import crawl
import time
import urllib2
from bs4 import BeautifulSoup

class Proxy(crawl.Crawl):
    def __init__(self,test_url = "http://www.baidu.com/"):
        self.domestic_proxy_url = "http://www.haodailiip.com/guonei/"
        self.timeout = 5
        self.testUrl = test_url

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

    def checkProxy(self,pages=3):
        cookies = urllib2.HTTPCookieProcessor()
        proxy_list = self.crawl_proxy(pages)
        checkedProxyList = []
        for proxy in proxy_list:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(proxy[0],proxy[1])})
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t1 = time.time()
            try:
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                if result != "" or None:
                    checkedProxyList.append((proxy[0],proxy[1],timeused))
                else:
                     continue
            except Exception,e:
                continue
        return checkedProxyList

    def pick_good_proxy(self,num=10):
        final_list = []
        proxy_list = self.checkProxy()
        ranked_proxy = sorted(proxy_list,key=lambda x:x[2])
        top_proxies = ranked_proxy[0:num]
        proxyfw = open("proxy list.txt","w")
        for proxy in top_proxies:
            prox = str(proxy[0]) + " " + str(proxy[1]) + "\n"
            proxyfw.write(prox)
            final_list.append([proxy[0],proxy[1]])
        proxyfw.close
        return final_list
