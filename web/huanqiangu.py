# coding:utf-8

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_html(url):
    head = {}
    # 使用代理
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    response = requests.post(url)
    return response.text

if __name__ == '__main__':
    # 第8章的网址
    url = 'http://www.136book.com/huaqiangu/'
    html = get_html(url)
    # 创建request对象
    soup = BeautifulSoup(html, 'lxml')
    # 找出div中的内容
    soup_text = soup.find('div', id = 'book_detail', class_='box1').find_next('div')
    f = open('D:/python/crawl/huanqiangu.txt', 'w')
    count = 1
    for link in soup_text.ol.children:
        if link != '\n':
            download_url = link.a.get('href')
            download_html = get_html(download_url)
            download_soup = BeautifulSoup(download_html, 'lxml')
            download_soup_texts = download_soup.find('div', id='content').select("p")
            for p in download_soup_texts:
                f.write(p.text)
                f.write('\n')
                count = count + 1
            f.write('\n\n')
        if count > 3:
            break
    f.close()

