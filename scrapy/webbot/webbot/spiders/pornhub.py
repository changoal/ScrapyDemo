# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re

from webbot.items import WebbotItem
from webbot.pornhub_type import PH_TYPES
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider


class PornhubSpider(CrawlSpider):
    name = 'pornhub'
    host = 'https://www.pornhub.com'
    allowed_domains = ['pornhub.com']
    start_urls = list(set(PH_TYPES))
    logging.getLogger("requests").setLevel(
        logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.DEBUG,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    # test = True
    def start_requests(self):
        for ph_type in self.start_urls:
            yield Request(
                url='https://www.pornhub.com/%s' % ph_type,
                callback=self.parse_ph_key)

    def parse_ph_key(self, response):
        selector = Selector(response)
        logging.debug('request url:------>' + response.url)
        # logging.info(selector)
        divs = selector.xpath('//div[@class="phimage"]')
        for div in divs:
            # logging.debug('divs :------>' + div.extract())

            viewkey = re.findall('viewkey=(.*?)"', div.extract())
            # logging.debug(viewkey)
            yield Request(
                url='https://www.pornhub.com/embed/%s' % viewkey[0],
                callback=self.parse_ph_info)
        url_next = selector.xpath(
            '//a[@class="orangeButton" and text()="Next "]/@href').extract()
        logging.debug(url_next)
        if url_next:
            # if self.test:
            logging.debug(' next page:---------->' + self.host + url_next[0])
            yield Request(
                url=self.host + url_next[0], callback=self.parse_ph_key)
            # self.test = False

    def parse_ph_info(self, response):
        phItem = WebbotItem()
        selector = Selector(response)
        # logging.info(selector)
        _ph_info = re.findall('var flashvars =(.*?),\n', selector.extract())
        logging.debug('PH信息的JSON:')
        logging.debug(_ph_info)
        _ph_info_json = json.loads(_ph_info[0])
        duration = _ph_info_json.get('video_duration')
        phItem['video_duration'] = duration
        title = _ph_info_json.get('video_title')
        phItem['video_title'] = title
        image_url = _ph_info_json.get('image_url')
        phItem['image_url'] = image_url
        link_url = _ph_info_json.get('link_url')
        phItem['link_url'] = link_url
        quality_480p = _ph_info_json.get('quality_480p')
        phItem['quality_480p'] = quality_480p
        logging.info('duration:' + duration + ' title:' + title +
                     ' image_url:' + image_url + ' link_url:' + link_url)
        yield phItem