#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: taobaomm

import os
import re
import sys

import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
PAGE_START = 1
PAGE_END = 30
DIR_PATH = 'D:/python/crawl/mm/'

absolute_url = 'https://mm.taobao.com/json/request_top_list.htm?page='


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = soup.find_all("a", class_='lady-avatar')
    return href_list


def get_jpg(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = soup.find_all("div", class_='lady-avatar')
    return href_list


# 创建保存图片的文件夹
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在    True
    # 不存在  Flase
    isExists = os.path.exists(path)
    if not isExists:
        print u'新建文件名为', path, u'的文件夹'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已经存在
        print u'名为', path, u'的文件夹已经创建成功'
        return False


def saveImg(content, path):
    try:
        image = requests.get("http:" + content).content
        f = open(path, 'wb')
        f.write(image)
        f.close()
    except:
        print 'exception'


def getImg(html, count):
    # 利用正则表达式把源代码中的图片地址过滤出来
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)  # 在整个网页中过滤出所有图片的地址，放在imglist中
    path = DIR_PATH + "%s" % count
    mkdir(path)
    x = 100
    for imgurl in imglist:
        if imgurl.startswith("//"):
            saveImg(imgurl, path + "/%s.jpg" % (x))  # 打开imgurl中的图片，并下载图片保存在本地
            x = x + 1
            print '正在保存照片'


if __name__ == '__main__':
    count = PAGE_START
    while count < PAGE_END:
        html = requests.get(absolute_url + "%s" % count).content
        comment_list = []
        # 获取超链接列表
        href_list = get_data(html, )
        for href_text in href_list:
            href = href_text.attrs['href']
            url = 'http:' + href
            html = requests.get(url).content
            getImg(html, count)
            count = count + 1
