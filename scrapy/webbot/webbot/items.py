# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class WebbotItem(scrapy.Item):
    video_title = Field()
    image_url = Field()
    video_duration = Field()
    quality_480p = Field()
    video_views = Field()
    video_rating = Field()
    link_url = Field()
