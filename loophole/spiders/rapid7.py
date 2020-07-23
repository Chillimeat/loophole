# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy import Request
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class Rapid7Spider(scrapy.Spider):
    name = 'rapid7'
    allowed_domains = ['rapid7.com']
    source = "https://www.rapid7.com"
    start_urls = ['https://www.rapid7.com/db/?']
    page = 1
    total = 20
    params = {
        "q": "",
        "type": "",
        "page": page
    }
    headers = {
        "Referer": "https://www.rapid7.com"
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))

        item = RepositoryItem()
        total_pages = response.xpath(
            '//section[@class="results-info"]/div/span[last()]/text()').extract_first("20").split(",")
        self.total = int("".join(total_pages))
        print(self.total)
        a_list = response.xpath('//section[@class="vulndb__results"]/a')
        for a in a_list:
            link = a.xpath('./@href').extract_first("")
            link = urljoin(self.source, link)
            title = a.xpath('./div/div[1]/text()').extract_first("").strip()
            source = self.source
            date = a.xpath('./div/div[2]/text()').extract_first("").strip().split("|")[0].strip().split(":")[-1].strip()
            pattern = r'CVE-\d{1,4}-\d{1,8}'
            cve = re.findall(pattern, title, re.I)
            cve = cve[0] if cve else ""
            item["title"] = title
            item["source"] = source
            item["date"] = date
            item["link"] = link
            item["cve"] = cve
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        self.page += 1
        self.params["page"] = self.page
        next_url = self.start_urls[0] + urlencode(self.params)
        # if self.page <= (int(self.total)//20 + 1):
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        cve = item.get('cve')
        div = response.xpath('//div[contains(@class,"vulndb__detail-main")]')
        description = div.xpath('./section[2]//text()').extract()
        description_list = [i.strip() for i in description if i.strip()]
        solutions = div.xpath('./section[3]//text()').extract()
        solutions_list = [j.strip() for j in solutions if j.strip()]
        related_vulnerabilities = div.xpath('./section[4]//text()').extract()
        related_vulnerabilities_list = [z.strip() for z in related_vulnerabilities if z.strip()]
        references = div.xpath('./section[5]//text()').extract()
        references_list = [x.strip() for x in references if x.strip()]
        info_list = [cve] + ['\n'] + description_list + ['\n'] + solutions_list + ['\n'] + related_vulnerabilities_list + ['\n'] + references_list
        info_str = '\n'.join(info_list)
        item['detail_info'] = info_str
        print(item)
        yield item



