#-*- coding:utf8 -*-
#coding=utf-8

import requests
import httplib
import socket
import sys
socket.setdefaulttimeout(10)

class Crawl():
    def get_url(self,url,tried_times=0):
        while tried_times < 5:
            try:
                source_code = requests.get(url)
                if str(source_code) == "<Response [200]>":
                    return source_code
            except socket.error:
                tried_times += 1
                self.get_url(url,tried_times)
            except requests.exceptions.Timeout:
                tried_times += 1
                self.get_url(url,tried_times)
            except requests.exceptions.ConnectionError:
                tried_times += 1
                self.get_url(url,tried_times)
            except httplib.IncompleteRead:
                tried_times += 1
                self.get_url(url,tried_times)
            except requests.exceptions.RequestException as e:
                print e
                sys.exit(1)
        return "error"

    def get_url_text(self,url,tried_times=0):
        while tried_times < 5:
            source_code = self.get_url(url)
            try:
                text = source_code.text
                return text
            except AttributeError:
                tried_times += 1
                self.get_url_text(url,tried_times)
        return "error"

    def seprate_set(self,sets=set(),num=1):
        current_set = sets
        result = []
        set_length = len(sets) / num + 1
        count = 1
        little_set = set()
        for s in current_set:
            if count < set_length:
                little_set.add(s)
                count += 1
            else:
                little_set.add(s)
                result.append(little_set)
                little_set = set()
                count = 1
        if not little_set == set():
            result.append(little_set)
        return result

    def create_class(self,name="name",num=1):
        result = []
        for i in range(1,num + 1):
            result.append(name + str(i))
        return result







