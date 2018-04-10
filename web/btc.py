#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#project baidu top10

import json
import os
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding('utf8')

absolute_url = 'https://www.baidu.com/s?ie=UTF-8&wd='
sava_path = 'D:/python/crawl/baidu/'


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


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    result_count = soup.find("div", class_='search_tool_conter').next_sibling.text
    result_list = soup.find_all("div", class_='result c-container ')
    return result_count, result_list


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


def saveContent(content, path):
    try:
        f = open(path, 'a')
        f.write(content + "\n")
        f.close()
    except:
        print 'exception'

def searchKeywordAndSave(keyword):
    html = get_html(absolute_url + keyword)
    result_count, result_list = get_data(html, )
    print result_count
    mkdir(sava_path)
    for result in result_list:
        result_detail = result.find_all('div', class_='c-tools')[0].attrs['data-tools']
        hjson = json.loads(result_detail)
        title = hjson['title']
        url = hjson['url']
        saveContent(title + "  " + url, sava_path + keyword + ".txt")

if __name__ == '__main__':
    keyword = "天气"
    searchKeywordAndSave(keyword)