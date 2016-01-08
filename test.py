#-*- coding:utf8 -*-
#coding=utf-8

import JD
import sys
import threading
import proxy
import crawl

reload(sys)
sys.setdefaultencoding('utf-8')

test = crawl.Crawl()
text = test.get_url_text_proxy("http://list.jd.com/list.html?cat=9987,653,655",["117.136.234.11", "843"],"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
print text