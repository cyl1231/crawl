#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: taobaomm

import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding('utf8')

sava_path = 'D:/python/crawl/tuchongMM/'
absolute_url = 'https://nothingq.tuchong.com/posts/'


def get_month_nav(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = soup.find_all(class_='time-month')
    return href_list


def get_album(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = soup.find_all(class_=re.compile("post-photo"))
    return href_list


def get_jpg(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = soup.find_all("div", class_='lady-avatar')
    return href_list


def get_html(url):
    params = DesiredCapabilities.PHANTOMJS  # 这本身是一个dict格式类属性
    params['phantomjs.page.settings.userAgent'] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
                                                   "(KHTML, like Gecko) Chrome/15.0.87")  # 在这个类属性里加上一个“phantomjs.page.settings.userAgent”
    driver = webdriver.PhantomJS(executable_path=r'D:\python\phantomjs-2.1.1-windows\bin\phantomjs.exe',
                                 desired_capabilities=params)
    driver.get(url)  # 这时候get方法请求的时候调用DesiredCapabilities.PHANTOMJS属性的时候就会用上指定的header
    time.sleep(2)
    content = driver.page_source
    return content


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
        image = requests.get(content).content
        f = open(path, 'wb')
        f.write(image)
        f.close()
    except:
        print 'exception'


def getImg(html, dir_path, count):
    # 利用正则表达式把源代码中的图片地址过滤出来
    reg = r'src="(https://photo.tuchong.com.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)  # 在整个网页中过滤出所有图片的地址，放在imglist中
    path = sava_path + dir_path
    mkdir(path + "/%s" % (count))
    img_count = 1
    for imgurl in imglist:
        saveImg(imgurl, path + "/%s" % (count) + "/%s.jpg" % (img_count))  # 打开imgurl中的图片，并下载图片保存在本地
        print imgurl
        img_count = img_count + 1
        print '正在保存照片' + path + "/%s" % (count) + "/%s.jpg" % (img_count)


if __name__ == '__main__':
    html = get_html("https://nothingq.tuchong.com/")
    comment_list = []
    # 获取超链接列表
    href_list = get_month_nav(html, )
    for href_text in href_list:
        href = href_text.attrs['href']
        dir_path = href.split("/")[4]
        html = get_html(href)
        album_content_list = get_album(html)
        count = 100
        for album_content in album_content_list:
            album_href = album_content.attrs['data-url']
            html = requests.get(album_href).content
            getImg(html, dir_path, count)
            count = count + 100
