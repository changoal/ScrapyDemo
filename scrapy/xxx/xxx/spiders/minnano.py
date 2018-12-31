# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from xxx.items import XxxItem


class MinnanoSpider(CrawlSpider):
    name = 'minnano'
    # allowed_domains = ['minnano-av.com']
    start_urls = ['http://www.minnano-av.com/']

    rules = [
        Rule(
            LinkExtractor(
                allow="http://www.minnano-av.com/actress(\d+).html", ),
            callback="parse_item",
            follow=True),
    ]

    def parse_item(self, response):
        item = XxxItem()
        names = []
        name = response.xpath(
            '//div[@class="act-profile"]/table/tr[1]/td/h2/text()')[
                0].extract()
        if name:
            names.append(name)

        item['_id'] = get_id_from_url(response.url)
        item['title'] = response.xpath("//h1/text()")[0].extract()
        item['img_url'] = response.xpath(
            '//div[@class="act-area"]//div[@class="thumb"]/img/@src')[
                0].extract()
        appearance = response.xpath(
            '//table[@class="rate-table"]/tr[1]/td[3]/text()').extract()
        if appearance:
            item['appearance'] = float(appearance[0])
        figure = response.xpath(
            '//table[@class="rate-table"]/tr[2]/td[3]/text()').extract()
        if figure:
            item['figure'] = float(figure[0])
        charm = response.xpath(
            '//table[@class="rate-table"]/tr[3]/td[3]/text()').extract()
        if charm:
            item['charm'] = float(charm[0])
        jue = response.xpath(
            '//table[@class="rate-table"]/tr[4]/td[3]/text()').extract()
        if jue:
            item['jue'] = float(jue[0])
        evaluation = response.xpath(
            '//table[@class="rate-table"]/tr[5]/td[3]/text()').extract()
        if evaluation:
            item['evaluation'] = float(evaluation[0])

        trs = response.xpath(
            '//div[@class="act-profile"]/table/tr/td[1]/span/text()')

        for i in range(len(trs)):
            if trs[i].extract() == '別名':
                name = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if name:
                    names.append(name[0])
            elif trs[i].extract() == '愛称':
                name = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if name:
                    names.append(name[0])
            elif trs[i].extract() == '生年月日':
                birthday = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if birthday:
                    item['birthday'] = str(birthday[0]).split("\n")[0]
                age = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if age:
                    item['age'] = str(age[0]).replace('歳', '')
            elif trs[i].extract() == 'サイズ':
                th = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if th:
                    size_str = ''
                    for t in th:
                        size_str = size_str + t
                    size = [
                        t.replace('(', '').replace(')', '')
                        for t in size_str.split() if not t is "/"
                    ]
                    item['size'] = size
            elif trs[i].extract() == '趣味・特技':
                hobby = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if hobby:
                    hobbyies = str(hobby[0]).split("、")
                    item['hobby'] = hobbyies
            elif trs[i].extract() == 'AV出演期間':
                start_time = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/text()'.
                    format(id=str(i + 2))).extract()
                if start_time:
                    item['start_time'] = start_time[0].split(" ")[0]
            elif trs[i].extract() == '血液型':
                blood_type = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if blood_type:
                    item['blood_type'] = blood_type[0]
            elif trs[i].extract() == '出身地':
                birthplace = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if birthplace:
                    item['birthplace'] = birthplace[0]
            elif trs[i].extract() == '所属事務所':
                office = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if office:
                    item['office'] = office[0]
                office_url = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/@href'.
                    format(id=str(i + 2))).extract()
                if office_url:
                    item['office_url'] = office_url[0]
            elif trs[i].extract() == 'ブログ':
                blog = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if blog:
                    item['blog'] = blog[0]
            elif trs[i].extract() == '公式サイト':
                website = response.xpath(
                    '//div[@class="act-profile"]/table/tr[{id}]/td/p/a/text()'.
                    format(id=str(i + 2))).extract()
                if website:
                    item['website'] = website[0]
            elif trs[i].extract() == 'タグ':
                tags = response.xpath(
                    '//div[@class="tagarea"]/a/text()').extract()
                item['tags'] = tags
        item['names'] = names
        print(item)
        yield item


def get_id_from_url(url):
    return url.replace('http://www.minnano-av.com/actress', '').replace(
        '.html', '')
