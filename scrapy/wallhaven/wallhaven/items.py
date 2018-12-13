# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WallhavenItem(scrapy.Item):
    _id = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    tags = scrapy.Field()
    uploader = scrapy.Field()
    favourites = scrapy.Field()
    Views = scrapy.Field()
    Size = scrapy.Field()
    time = scrapy.Field()
    img_url = scrapy.Field()
