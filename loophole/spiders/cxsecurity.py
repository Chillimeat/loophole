# -*- coding: utf-8 -*-
import scrapy
import feedparser
import re
from copy import deepcopy
from loophole.items import RepositoryItem


class CxsecuritySpider(scrapy.Spider):
    name = 'cxsecurity'
    allowed_domains = ['cxsecurity.com']
    start_urls = ['https://cxsecurity.com/cverss/fullmap/']

    def parse(self, response):
        item = RepositoryItem()
        buf = feedparser.parse(self.start_urls[0])
        # print(buf.entries)
        pattern = '(CVE-\d*?-\d*?)\D'
        for i in buf.entries:
            try:
                cve_list = re.findall(pattern, i.title, re.I)
                cve = cve_list[0] if cve_list else ''
                title = i.title
                link = i.link
                date = i.published
                detail_info = cve + '\n\n' + 'description\n' + i.summary
                source = 'https://cxsecurity.com'
                item["cve"] = cve
                item["title"] = title
                item["link"] = link
                item["date"] = date
                item["source"] = source
                item['download_id'] = 0
                item['type'] = ''
                item['author'] = ''
                item['platform'] = ''
                item['verified'] = ''
                item['detail_info'] = detail_info
                print(item)
                yield deepcopy(item)
            except Exception as ex:
                print(f'{ex}')

