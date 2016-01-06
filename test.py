#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import Proxy
import crawl

reload(sys)
sys.setdefaultencoding('utf-8')



list = [[u'221.176.14.72', u'80',0.1], [u'124.192.215.126', u'3128',1], [u'119.147.115.6', u'8088',14], [u'115.231.102.251', u'3128',22], [u'180.76.151.210', u'80',4], [u'183.239.173.138', u'8080',6]]
proxy = Proxy.crawl_Proxy()
proxy.pick_good_proxy()
#list = proxy.crawl_proxy(1)
#print list
#print len(list)
#check = Proxy.ProxyCheck(list)
#check.start()
