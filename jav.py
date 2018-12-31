import requests
import os
from lxml import etree
from bs4 import BeautifulSoup
import re

url = "http://javip.net/page/1/?s=FC+2+PPV+"

proxies = {"http": "http://50.116.53.171:80"}

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

    root = etree.HTML(res.content)

    posts = root.xpath("//div[@class='post']")
    for post in posts:
        print(post.xpath("/a/text()"))


def spider():
    res = requests.get(url, headers=headers, proxies=proxies)
    handler_bs4(res)


def get_post_info_by_str(msg):
    data = {}
    msgs = msg.split('\n')
    for m in msgs:
        if (m.startswith('販売�? ')):
            data['date'] = m.replace('販売�? ', '')
        elif (m.startswith('販売�? ')):
            data['author'] = m.replace('販売�? ', '')
        elif (m.startswith('再生時間 ')):
            data['length'] = m.replace('再生時間 ', '')
        elif (m.startswith('評価 ')):
            data['comment'] = m.replace('評価 ', '')
        elif (m.startswith('出演者： ')):
            data['actress'] = m.replace('出演者： ', '')
        elif (m.startswith('収録時間�? ')):
            data['length'] = m.replace('収録時間�? ', '')
        elif (m.startswith('レーベル�? ')):
            data['label'] = m.replace('レーベル�? ', '')
        elif (m.startswith('ジャンル�? ')):
            data['tag'] = m.replace('ジャンル�? ', '')
    print(data)


def get_post_info_by_re(msg):
    pattern = r"/w+"
    pass


summary = """
タイトル: 【鬼チンポｘ素人】生ちんぽ交尾編●発情おまんこ娘 ゆうこワ�? (仮名)２３�? 本気汁がダ�?
ダラ垂れるまんこに生ちんぽで発情した犬みたいにガツガツ交尾！大量中出し【個人撮影�?
評価 5
レビュー 57�?
販売�? 2017/05/15
販売�? 心斎橋ハードコア
再生時間 48:56
出演者： 青木�?
収録時間�? 120�?
レーベル�? Madonna
ジャンル�? 熟女 人妻 不�? スレンダ�? 単体作品 寝取り・寝取られ デジ�? サンプル動画
"""

if __name__ == '__main__':
    spider()
    # get_post_info_by_str(summary)
