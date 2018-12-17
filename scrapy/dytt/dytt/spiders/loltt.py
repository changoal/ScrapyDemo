# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LolttSpider(CrawlSpider):
    name = 'loltt'
    allowed_domains = ['dytt789.com']
    start_urls = ['https://www.dytt789.com/']

    rules = (Rule(
        LinkExtractor(
            allow='https://www.dytt789.com/(\w+)/(\w+)/$',
            deny='https://www.dytt789.com/(\w+)/$'),
        callback='parse_item',
        follow=False), )

    def parse_item(self, response):
        title = response.xpath("//h1/a/text()").extract()
        summary = response.xpath("//div[@class='neirong']/p/text()").extract()
        starring = response.xpath(
            "//div[@class='zhuyan']/ul/li[1]/text()").extract()
        print(
            response.xpath("//div[@class='zhuyan']/ul/li[1]/text()").extract())
