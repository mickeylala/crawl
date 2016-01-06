#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import Proxy
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlJD(threading.Thread,JD.JD_crawl):

    def __init__(self,sets=set(),num = 1):
        threading.Thread.__init__(self)
        JD.JD_crawl.__init__(self)
        self.crawl_set = sets
        self.num_of_thread = num

    def run(self):
        for i in self.crawl_set:
            self.crawl_from_catalog(i[0],i[1])

proxy = Proxy.crawl_Proxy()
list = proxy.crawl_proxy(10)
for i in list:
    print i[0] + " " + str(i[1])


'''
jd = CrawlJD()
threads = jd.create_class("JD",6)
sets = jd.seprate_set(jd.crawl_sort_page(),6)
combined =zip(threads, sets)
for thread,set in combined:
    thread = CrawlJD(set)
    thread.start()
'''




