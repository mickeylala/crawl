#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import proxy
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlJD(threading.Thread,JD.JD_crawl):

    def __init__(self,proxy_list,sets=set(),num = 1):
        threading.Thread.__init__(self)
        JD.JD_crawl.__init__(self)
        self.crawl_set = sets
        self.num_of_thread = num
        self.proxy_list = proxy_list

    def run(self):
        for i in self.crawl_set:
            self.crawl_from_catalog(i[0],self.proxy_list,i[1])



proxy = proxy.crawl_Proxy()
list = proxy.crawl_proxy(10)


jd = CrawlJD(list)
threads = jd.create_class("JD",10)
sets = jd.seprate_set(jd.crawl_sort_page(),10)
combined =zip(threads, sets)
for thread,set in combined:
    thread = CrawlJD(set)
    thread.start()
