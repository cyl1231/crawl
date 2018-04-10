# coding:utf-8
import random
import sys
import time

import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

absolute = 'https://movie.douban.com/subject/26322642/comments'
absolute_url = 'https://movie.douban.com/subject/26322642/comments?start=21&limit=20&sort=new_score&status=P&percent_type='
url = 'https://movie.douban.com/subject/26322642/comments?start={}&limit=20&sort=new_score&status=P'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
          'Connection': 'keep-alive'}


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    comment_list = soup.select('.comment > p')
    next_page = soup.select('#paginator > a')[2].get('href')
    date_nodes = soup.select('..comment-time')
    star_list = soup.find_all("span",class_='rating')
    return comment_list, next_page, date_nodes, star_list


if __name__ == '__main__':
    f_cookies = open('cookie.txt', 'r')
    cookies = {}
    for line in f_cookies.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    html = requests.get(absolute_url, cookies=cookies, headers=header).content
    comment_list = []
    # 获取评论
    comment_list, next_page, date_nodes, star_list = get_data(html, )
    soup = BeautifulSoup(html, 'lxml')
    comment_list = []
    while (next_page != []):  # 查看“下一页”的A标签链接
        print(absolute + next_page)
        html = requests.get(absolute + next_page, cookies=cookies, headers=header).content
        soup = BeautifulSoup(html, 'lxml')
        comment_list, next_page, date_nodes, star_list = get_data(html)
        f = open('D:/python/crawl/comments.txt', 'a')
        count = -1
        for node in comment_list:
            comment = node.get_text().strip().replace("\n", "")
            count = count + 1
            date = date_nodes[count].get_text().strip()
            star = star_list[count].attrs['class'][0]
            f.write(date)
            f.write(' ')
            f.write(star)
            f.write(' ')
            f.write(comment)
            f.write('\n')
        time.sleep(1 + float(random.randint(1, 100)) / 20)
    f.close()
