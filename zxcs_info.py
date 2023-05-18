# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# coding=utf-8

import re    # 正则表达式 进行文字匹配
from lxml import etree
import xlwt       # 进行excel 操作
import sqlite3    # sqlite3 数据库 操作
import requests
import pandas as pd
import time
import datetime


def main():


    # 1 爬取网页
    max_novel=get_max()

    # 2 解析数据
    result = dealData(6000, max_novel)
    # print(result)
    # 3 保存数据
    write2Csv(result)
    write2X(result)
    # write2db(result)


def get_max():
    """
    获取最新收录的小说的编号
    :return:
    """
    url_oringal = 'http://www.zxcs.info/'
    response = ask_url(url_oringal)
    response.encoding = 'utf8'
    html = etree.HTML(text=response.text)
    max_url = html.xpath('/html/body/div[4]/div[1]/div[2]/ul/li[1]/a/@href')
    max_num = max_url[0].split('/')
    return max_num[-1]


def get_name(number):
    """
    提取小说的书名和作者
    :param number: 小说编号
    :return: 书名和作者
    """
    # list=[]
    # list.append(number)
    url = 'http://zxcs.info/post/'
    novel_url = url+number
    response = ask_url(novel_url)
    response.encoding = 'utf8'
    html = etree.HTML(text=response.text)

    title = html.xpath('//*[@id="ptop"]/a[4]/text()')

    find_name = re.compile(r'《(.*)》')      # 提取书名,即<<>>之间的内容
    name = re.findall(find_name,title[0])[0]
    try:
        find_author = re.compile(r'作者:(.+)')  # 半角:
        author = re.findall(find_author, title[0])[0]  # 提取作者
    except:
        find_author = re.compile(r'作者：(.+)')  # 全角:
        author = re.findall(find_author, title[0])[0]  # 提取作者
    list = [number,name.strip(),author.strip()]
    return list


def get_rank(number):
    """
    获取小说的评价(投票的结果)
    :param number:
    :return: 投票的结果
    """
    voteurl = 'http://www.zxcs.info/content/plugins/cgz_xinqing/cgz_xinqing_action.php?action=show&id={}'.format(number)
    vote_html = requests.get(voteurl, headers=head)
    data1 = vote_html.text
    data_split = data1.split(",")
    # print(data_split)
    rank_data = []
    for item in data_split:
        rank = int(item)
        rank_data.append(rank)
    # print(rank_data)
    return rank_data


def ask_url(url):
    try:
        response = requests.get(url = url,headers = head)
    except:
        print("not found the page...")
    return response


def dealData (start,number):
    """
    抓取网页的数据
    :param start: 开始的小说标号
    :param number: 最后的小说标号
    :return: 结果的列表
    """
    result = []
    for i in range(start,int(number)):
        data=[]
        try:
            name = get_name(str(i))
            print(name)
            rank = get_rank(str(i))
            print(rank)
            data=name+rank
            result.append(data)
            print(i)
            time.sleep(1)
        except:
            print("there is no data {}".format(i))
            continue
    return result


def write2Csv(datalist):
    cols=['序列','书名','作者','仙草','粮草' ,'干草', '枯草', '毒草']
    df = pd.DataFrame(datalist,columns=cols)
    filename = "zxcs_info_"+today+".csv"
    df.to_csv(filename,encoding="utf_8_sig")


def write2X(datalist) :
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    # print(datalist)
    col = ("序列", "书名", "作者", "仙草", "粮草", "干草", "枯草", "毒草")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])
    for i in range(len(datalist)):
        for j in range(0, 8):
            worksheet.write(i+1, j, datalist[i][j])
    # savepath1 = ".\\book.xls"
    filename  = "zxcs_info_"+today+".xls"
    workbook.save(filename)


def db_init():
    conn = sqlite3.connect("zxcsa.db")
    cursor = conn.cursor()
    sqlcreat = '''
     create table booklist
     (
     numberX integer,
     title text,
     author text,
     xian integer ,
     liang integer ,
     gan integer,
     ku integer,
     du integer)
        '''
    cursor.execute(sqlcreat)
    conn.commit()
    conn.close()


def write2db(datalist):

    # db_init()
    conn=sqlite3.connect("zxcsa.db")

    cursor = conn.cursor()
    for data in datalist:
        cursor.execute("insert into booklist values(?,?,?,?,?,?,?,?)",data)
        conn.commit()
    conn.close()



if __name__ == '__main__':
    head = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58"
    }  # 用户代理,告诉服务器浏览器的类型

    today = datetime.datetime.today().strftime("%Y%m%d")


    main()


