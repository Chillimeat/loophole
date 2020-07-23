# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LoopholeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class RepositoryItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    cve = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    download_id = scrapy.Field()
    author = scrapy.Field()
    type = scrapy.Field()
    platform = scrapy.Field()
    verified = scrapy.Field()
    detail_info = scrapy.Field()




