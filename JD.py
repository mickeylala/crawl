#-*- coding:utf8 -*-
#coding=utf-8

import ast
import random
import proxy
from bs4 import BeautifulSoup

class JD_crawl(proxy.Proxy):
    next_page = "下一页"
    invalid_sign = "抱歉，没有找到相关的商品"

    def __init__(self):
        proxy.Proxy.__init__(self)
        self.sort_page = "http://www.jd.com/allSort.aspx"
        self.agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",
            "User-Agent	Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"
        ]

    def crawl_from_catalog(self,cat,proxy_list,filename="default",max_pages=50000,):
        page = 1
        proxy = self.open_proxy(proxy_list)
        agent = self.open_agent()
        ch_filename = filename.replace("/","&")
        path = "./links/" +  str(ch_filename) + ".txt"
        path = path.decode('utf-8').encode('cp936')
        fw = open(path,'a')
        while page <= max_pages:
            list_url = "http://list.jd.com/list.html?cat=" + str(cat) + "&page=" + str(page) + "&JL=6_0_0"
            plain_text = self.get_url_text_proxy(list_url,proxy,agent)
            urls = self.get_all_product_links_from_catalog(plain_text)
            if self.is_this_page_valid(plain_text):
                urls = self.get_all_product_links_from_catalog(plain_text)
                for link in urls:
                    result =link + "\n"
                    fw.write(result)
            else:
                break
            if not self.is_next_page_valid(plain_text):
                break
            page += 1
        fw.close
        fp = open("crawled.txt","w")
        cats = str(cat) + " "
        fp.write(cats)
        fp.close()
        print "%s crawling finished!" %filename

    def get_all_product_links_from_catalog(self,text):
        urls = []
        soup = BeautifulSoup(text,"html.parser")
        for link in soup.find_all("li",{"class": "gl-item"},):
            href = link.div.a.get("href")
            urls.append(href)
        return urls

    def crawl_sort_page(self):
        cats = set()
        plain_text = self.get_url_text(self.sort_page)
        soup = BeautifulSoup(plain_text,"html.parser")
        for link in soup.find_all("a"):
            cat_link = str(link.get("href"))
            cat_name = str(link.string).decode("utf-8")
            if "http://list.jd.com/list.html?cat=" in cat_link:
                catalog = cat_link.replace("http://list.jd.com/list.html?cat=","")
                cat_info = (catalog,cat_name)
                cats.add(cat_info)
        return cats

    def get_product_name(self,url,tried_times=0):
        while tried_times < 5:
            text = self.get_url_text(url)
            soup = BeautifulSoup(text,"html.parser")
            try:
                name = str(soup.find(id="name").h1)
                if name == "" or name == "None":
                    tried_times += 1
                    self.get_product_name(url,tried_times)
                else:
                    name = name[4:-5]
                    name = name.replace("\n","").strip()
                    return name
            except AttributeError:
                tried_times += 1
                self.get_product_name(url,tried_times)
        return "error"


    def get_sku(self,url):
        if "https" in url:
            return url[20:-5]
        else:
            return url[19:-5]

    def get_price(self,url,tried_times=0):
        while tried_times < 5:
            skuid = self.get_sku(url)
            price_link = "http://p.3.cn/prices/mgets?skuIds=J_" + skuid + "&type=1"
            plain_price = self.get_url_text(price_link)[1:-2]
            try:
                plain_price_dic = ast.literal_eval(plain_price)
            except ValueError:
                self.get_price(url,tried_times)
            if plain_price_dic["p"]:
                return plain_price_dic["p"]
            else:
                tried_times += 1
                self.get_price(url,tried_times)
        return "error"

    def is_this_page_valid(self,text):
        if self.invalid_sign in text:
            return False
        else:
            return True

    def is_next_page_valid(self,text):
        if self.next_page in text:
            return True
        else:
            return False

    def open_proxy(self,proxy_list):
        proxy = random.choice(proxy_list)
        return proxy

    def open_agent(self):
        agent = random.choice(self.agent_list)
        return agent
