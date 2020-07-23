# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from urllib.parse import urljoin
from datetime import datetime
from copy import deepcopy

from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class WinicssecSpider(scrapy.Spider):
    name = 'winicssec'
    allowed_domains = ['ivd.winicssec.com']
    source = 'http://ivd.winicssec.com'
    start_urls = ['http://ivd.winicssec.com/']
    page = 1
    headers = {
        'Referer': 'http://ivd.winicssec.com'
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))
        item = RepositoryItem()
        tr_list_xpath = '//table[@id="simple-table"]/tbody/tr'
        tr_list = response.xpath(tr_list_xpath)
        for tr in tr_list:
            title = tr.xpath('./td[1]/a/text()').extract()
            link = tr.xpath('./td[1]/a/@href').extract()
            link = urljoin(self.source, link[0])
            cve = tr.xpath('./td[3]/a/text()').extract()
            if not cve:
                continue
            source = self.source
            date = tr.xpath('./td[7]/text()').extract()
            item["title"] = title[0] if title else "no_title"
            item["link"] = link
            item["cve"] = cve[0]
            item["source"] = source
            item["date"] = date[0] if date else datetime.now().strftime("%Y-%m-%d")
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        # next_url = response.xpath(
        #     '//div[contains(@class,"col-xs-12")]/div/a[contains(@class,"next")]/@href').extract_first(" ")
        # if next_url:
        self.page += 1
        next_url = urljoin(self.source, 'index.php/Home/Index/index/p/{}.html'.format(self.page))
        if self.page <= TOTAL_PAGES:
            next_url = urljoin(self.source, next_url)
            yield Request(url=next_url, headers=self.headers, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        cve = item.get('cve')
        div_list = response.xpath('//div[@class="container"]/div')
        infos = []
        for div in div_list[3:]:
            info_list = div.xpath('.//text()').extract()
            info = '\n'.join([i.strip() for i in info_list if i.strip()])
            # print(info)
            infos.append(info)
            infos.append('\n')
        info_str = '\n'.join(infos)
        detail_info = cve + "\n\n" + info_str
        item['detail_info'] = detail_info
        print(item)
        yield item



