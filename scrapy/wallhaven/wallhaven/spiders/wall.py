# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from wallhaven.items import WallhavenItem
import pymongo


class WallSpider(scrapy.Spider):
    name = 'wall'
    # allowed_domains = ['wallhaven.cc']
    start_urls = [
        'https://alpha.wallhaven.cc/latest?page=%s' % str(i)
        for i in range(1, 14445)
    ]

    collection = pymongo.MongoClient('localhost', 27017)['wallhaven']['wall']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        section_soup = soup.find('section', class_='thumb-listing-page')
        if section_soup:
            ul_soup = section_soup.find('ul')
            if ul_soup:
                lis = ul_soup.find_all('li')
                for li in lis:
                    a_soup = li.find('a', class_='preview')['href']
                    img_id = a_soup.split('/')[-1]
                    yield Request(a_soup, callback=self.parse_image)
            else:
                print("not found ul")
        else:
            print("not found thumb-listing-page")

    def parse_image(self, response):
        data = WallhavenItem()
        data['_id'] = response.url.split('/')[-1]
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            resolution = soup.find(
                'h3', class_='showcase-resolution').get_text()
            if resolution:
                splits = resolution.split('x')
                if len(splits) == 2:
                    data['width'] = splits[0].strip()
                    data['height'] = splits[1].strip()
            tags_ul = soup.find('ul', id='tags')
            if tags_ul:
                tags_lis = tags_ul.find_all('li')
                tags = []
                for tag in tags_lis:
                    tags.append(tag.get_text())
                data['tags'] = tags
            uploader = soup.find('a', class_='username usergroup-2').get_text()
            data['uploader'] = uploader
            favourites = soup.find('a', class_='overlay-anchor').get_text()
            showcase = soup.find(
                'div', attrs={'data-storage-id': 'showcase-info'})
            dl_soup = showcase.find('dl')
            dds = dl_soup.find_all('dd')
            data['favourites'] = dds[-1].get_text().strip()
            data['Views'] = dds[-2].get_text().strip()
            data['Size'] = dds[-3].get_text().strip()
            time = dl_soup.find('time')['title']
            data['time'] = time
            image = soup.find('img', id='wallpaper')['src']
            data['img_url'] = image
        except Exception as e:
            print(e)
        else:
            yield data
