# coding:utf-8

import sys
import time

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


def crawl_mail():
    url = 'https://www.huobi.pro/zh-cn/eos_usdt/exchange/'
    html = get_html(url)
    # 创建request对象
    soup = BeautifulSoup(html, 'lxml')
    # 找出div中的内容
    soup_text = soup.find('div', class_='coin_list')
    btc, eth, eos, xrp = process_result(soup_text.text.strip())
    send_text = btc + " |" + eth + " |" + eos + " |" + xrp
    print send_text
    mail.sendMail(send_text.encode("utf-8"))


if __name__ == '__main__':
    while 1:
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print date
        crawl_mail()
        time.sleep(10 * 60)
