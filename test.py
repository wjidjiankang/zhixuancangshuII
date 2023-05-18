import re    # 正则表达式 进行文字匹配
import urllib.request   # 指定url 获取网页数据
from bs4 import BeautifulSoup    #网页解析,获取数据
import lxml
import xlwt       # 进行excel 操作
import sqlite3    # sqlite3 数据库 操作
import requests
import pandas as pd
import time
from lxml import etree

head = {  # 模拟浏览器头部信息
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58"
    }  # 用户代理,告诉服务器浏览器的类型

import datetime

# today = datetime.datetime.today().strftime("%Y%m%d")
# print(type(today))
# s = str(today)
# print(s)
#
def ask_url(url):
    try:
        response = requests.get(url = url,headers = head)
    except requests.exceptions :
        print("not found the page...")
    return response


number = '10927'
url = 'http://zxcs.me/post/'
novel_url = url+number
response = ask_url(novel_url)
response.encoding = 'utf8'
html = etree.HTML(text=response.text)

title = html.xpath('//*[@id="ptop"]/a[4]/text()')

find_name = re.compile(r'《(.*)》')      # 提取书名,即<<>>之间的内容
name = re.findall(find_name,title[0])[0]
try :
    find_author = re.compile(r'作者:(.+)')   #半角:
    author = re.findall(find_author,title[0])[0]  #提取作者
except:
    find_author = re.compile(r'作者：(.+)') # 全角:
    author = re.findall(find_author,title[0])[0]  #提取作者
list = [number,name.strip(),author.strip()]
# return list
print(list)


