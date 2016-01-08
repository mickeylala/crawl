#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import proxy
import crawl

reload(sys)
sys.setdefaultencoding('utf-8')

'''
proxy = proxy.Proxy()
proxy.pick_good_proxy()
'''


proxy = ["10.131.64.125","80"]
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0"
test = crawl.Crawl()
a = test.get_url_proxy("http://item.jd.com/1856588.html",proxy,agent)
print a.read()
