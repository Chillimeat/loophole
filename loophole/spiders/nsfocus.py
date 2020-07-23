# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy.http import Request
from urllib.parse import urljoin
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class NsfocusSpider(scrapy.Spider):
    name = 'nsfocus'
    allowed_domains = ['nsfocus.net']
    source = "http://www.nsfocus.net"
    page = 1
    param_str = "&type_id=&os=&keyword=&page={}".format(page)
    start_urls = ['http://www.nsfocus.net/index.php?act=sec_bug']
    headers = {
        "Referer": "http://www.nsfocus.net"
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))

        item = RepositoryItem()
        li_list = response.xpath('//div[@class="vulbar"]/ul/li')
        for li in li_list:
            date = li.xpath('./span/text()').extract_first(" ")
            title = li.xpath('./a/text()').extract_first(" ")
            link = li.xpath('./a/@href').extract_first(" ")
            link = urljoin(self.source, link)
            source = self.source
            pattern = "(CVE-\d{4}-\d{0,15})"
            cve = re.findall(pattern, title, re.I)
            cve = cve[0] if cve else ""
            if not cve:
                continue
            item["title"] = title
            item["cve"] = cve
            item["link"] = link
            item["source"] = source
            item["date"] = date
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        next_url = response.xpath('//div[@class="contents"]/div/a[@title="Next"]/@href').extract_first("")
        next_url = urljoin(self.source, next_url)
        last_url = response.xpath('//div[@class="contents"]/div/a[@class="last"]/@href').extract_first("")
        last_url = urljoin(self.source, last_url)
        total_page = int(last_url.split("=")[-1])
        # current_page = int(next_url.split("=")[-1])
        # print("正在爬取第{}页：".format(current_page))
        self.page += 1
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)
        else:
            print("总页数为：", total_page)

    def parse_detail(self, response):
        item = response.meta.get('item')
        # cve = item.get('cve')
        # if not cve:
        #     cve = response.xpath('//div[@class="vulbar"]/a[1]/text()').extract_first("")
        #     item['cve'] = cve
        div = response.xpath('//div[@class="vulbar"]//text()').extract()
        info_list = [i.strip() for i in div if i.strip()]
        info_str = '\n'.join(info_list)
        detail_info = item.get('cve') + "\n\n" + info_str
        item['detail_info'] = detail_info
        print(item)
        yield item



