#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import Proxy
import crawl

reload(sys)
sys.setdefaultencoding('utf-8')


proxy = Proxy.crawl_Proxy()
proxy.pick_good_proxy()
#list = proxy.crawl_proxy(1)
#print list
#print len(list)
#check = Proxy.ProxyCheck(list)
#check.start()
