# -*- coding: UTF-8 -*-
import urllib3
import urllib.request
import urllib
from lxml import etree
import json

class yami_crawler:

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'cookie': 'X-Salesforce-CHAT=!rlG9xhs+/lxiRpnSDPVgNVwHDUwQ9cQrpzsfl003y2Pl1lj0YfsnHeRHAXfxmT4PlxhSNqRdSYhW4k0='
        }


    def __init__(self, name):
        self.name = name
        key = urllib.parse.quote(self.name)
        url_pre = "https://www.yamibuy.com/zh/search?q="
        self.url = url_pre + key



    def page_generate(self):
        url_request = urllib.request.Request(self.url, None, self.headers)
        response = urllib.request.urlopen(url_request).read()
        selector = etree.HTML(response)
        json_data = json.loads(selector.xpath("//*[@id='itemsData']/@value")[0])

        return json_data
        
    def data_output(self, json_data, sum):
        good_list = []
        for data in json_data:
            if(sum == 0): break
            good_name = data["goods_name"]
            if(data["goods_number"] != 0):
                good_number = " in stock"
            else:
                good_number = " out of stock"
            good_list.append(good_name+good_number)
            
            sum -= 1
            
        return good_list


""" a = yami_crawler("话梅")
c = a.page_generate()
print(a.data_output(c,3)) """

