# coding:utf-8

import Queue
import re
import sys
import time
from pyecharts import Line
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from util import mail

reload(sys)
sys.setdefaultencoding('utf8')


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


def process_result(result):
    strings = result.split("       ")
    datas = strings[1].split("      ")
    btc = datas[0]
    eth = datas[2]
    eos = datas[5]
    xrp = datas[6]
    return btc, eth, eos, xrp

def alertMail(increase, price ,send_text):

    increase_reate = re.findall(r"\d+\.?\d*", increase)
    send_flag = 0
    if float(price) > 8500.0:
        send_flag = 1
    if float(increase_reate[0]) > 10.0:
        send_flag = 2
    if send_flag > 0:
        if send_flag == 1:
            print "btc price trigger mail"
        elif send_flag == 2:
            print "increase trigger mail"
        mail.sendMail(send_text.encode("utf-8"))

def crawl_mail(workQueue):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    attrs.append(date)
    url = 'https://www.huobi.pro/zh-cn/eos_usdt/exchange/'
    html = get_html(url)
    # 创建request对象
    soup = BeautifulSoup(html, 'lxml')
    # 找出div中的内容
    soup_text = soup.find('div', class_='coin_list')
    btc, eth, eos, xrp = process_result(soup_text.text.strip())
    send_text = btc + " |" + eth + " |" + eos + " |" + xrp
    print send_text
    workQueue.put(btc)
    workQueue.put(eth)
    workQueue.put(eos)
    workQueue.put(xrp)
    while workQueue.qsize() > 0:
        print workQueue.qsize()
        coin = workQueue.get()
        results = coin.split(" ")
        name = results[0]
        price = results[1]
        increase = results[2]
        if cmp(name, "btc") == 0:
            btcs.append(price)
        elif cmp(name, "eos") == 0:
            eoss.append(price)
        elif cmp(name, "eth") == 0:
            eths.append(price)
        elif cmp(name, "xrp") == 0:
            xrps.append(price)
        alertMail(increase, price, send_text)
    line = Line("huobi 主区大盘btc")
    line.add("btc", attrs, btcs, is_smooth=True, mark_line=["max", "average"])
    line.show_config()
    line.render()


if __name__ == '__main__':
    workQueue = Queue.Queue(10)
    attrs = []
    btcs = []
    eths = []
    eoss = []
    xrps = []
    count = 1
    while 1:
        print str(count)
        count += 1
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print date
        crawl_mail(workQueue)
        time.sleep(10)
