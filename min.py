import requests
import os
from lxml import etree
from bs4 import BeautifulSoup
import re

url = "http://www.minnano-av.com/actress411935.html"

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def handler_bs4(response):
    soup = BeautifulSoup(response.text, 'lxml')
    posts = soup.find_all('div', class_='post')
    for post in posts:
        title = post.find('h2').find('a').get_text()
        author = post.find('span', class_='p_author').get_text()
        date = post.find('span', class_='p_date').get_text()
        comment = post.find('span', class_='p_comment').get_text()
        url = post.find('a', class_='more-link')['href']
        img = post.find_all('p')[1].find('img')['src']
        summary = post.find_all('p')[1].get_text()
        print(title, author, date, comment, url, img, summary, sep="\n")
        print("=" * 30)


def handler_xpath(response):

    response = etree.HTML(response.content)

    title = response.xpath("//h1/text()")[0]
    print('title', title)
    img = response.xpath(
        '//div[@class="act-area"]//div[@class="thumb"]/img/@src')[0]
    print('img', img)
    face = response.xpath('//table[@class="rate-table"]/tr[1]/td[3]/text()')
    if face:
        print('face', float(face[0]))
    body = response.xpath('//table[@class="rate-table"]/tr[2]/td[3]/text()')
    if body:
        print('body', float(body[0]))
    mei = response.xpath('//table[@class="rate-table"]/tr[3]/td[3]/text()')
    print('mei', mei)
    jue = response.xpath('//table[@class="rate-table"]/tr[4]/td[3]/text()')
    print('jue', jue)
    total = response.xpath('//table[@class="rate-table"]/tr[5]/td[3]/text()')
    if total:
        print('total', float(total[0]))
    names = []
    name = response.xpath(
        '//div[@class="act-profile"]/table/tr[1]/td/h2/text()')[0]
    names.append(name)
    trs = response.xpath(
        '//div[@class="act-profile"]/table/tr/td[1]/span/text()')
    for i in range(len(trs)):
        if trs[i] == '別名':
            names.append(
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == '生年月日':
            print(
                'birthday',
                str(
                    response.xpath(
                        '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                        format(id=str(i + 2)))[0]).split("\n")[0])
            print(
                'age',
                str(
                    response.xpath(
                        '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                        format(id=str(i + 2)))[0]).replace('歳', ''))
        elif trs[i] == 'サイズ':

            th = response.xpath(
                '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                format(id=str(i + 2)))
            aaa = ''
            for t in th:
                aaa = aaa + t
            threewei = [
                t.replace('(', '').replace(')', '') for t in aaa.split()
                if not t is "/"
            ]
            print('threewei', threewei)
        elif trs[i] == '趣味・特技':
            hobby = response.xpath(
                '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                format(id=str(i + 2)))[0]
            hobbyies = str(hobby).split("、")
            print('hobby', hobbyies)
        elif trs[i] == 'AV出演期間':
            print(
                'start_time',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2)))[0].split(" ")[0])
        elif trs[i] == '血液型':
            print(
                'bolld_type',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == '出身地':
            print(
                'place',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == '所属事務所':
            print(
                'office',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == 'ブログ':
            print(
                'blog',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == '公式サイト':
            print(
                'website',
                response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2)))[0])
        elif trs[i] == 'タグ':
            tags = response.xpath('//div[@class="tagarea"]/a/text()')
            print('tags', tags)
    print('name', names)


def spider():
    res = requests.get(url, headers=headers)
    handler_xpath(res)


if __name__ == '__main__':
    spider()
    # get_post_info_by_str(summary)
