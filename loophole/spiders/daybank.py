# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy.http import Request
from urllib.parse import urljoin
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class DaybankSpider(scrapy.Spider):
    name = 'daybank'
    allowed_domains = ['0daybank.org']
    source = 'http://www.0daybank.org'
    page = 1
    param_str = "/?paged={}&cat=11"
    start_urls = [urljoin(source, param_str.format(page))]
    headers = {
        "Referer": "http://www.0daybank.org"
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))
        item = RepositoryItem()
        div_list_xpath = '//div[@id="post-wrapper"]/div'
        div_list = response.xpath(div_list_xpath)
        for div in div_list:
            title = div.xpath('./article/header/h2/a/text()').extract()
            date = div.xpath('./article/header/div/span/a/time/text()').extract()
            link = div.xpath('./article/header/h2/a/@href').extract()
            pattern = '(CVE-\d{4}-\d{0,9})'
            cve = re.findall(pattern, title[0] if title else "", re.I)
            if not cve:
                continue
            source = self.source
            item["title"] = title[0] if title else ""
            item["date"] = date[0]
            item["link"] = link[0]
            item["cve"] = cve[0] if cve else ""
            item["source"] = source
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link[0], meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        # next_url = response.xpath('//nav/div/a[contains(@class,"next")]/@href').extract_first("")
        # if next_url:
        self.page += 1
        next_url = urljoin(self.source, self.param_str.format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        div = response.xpath('//div[contains(@class,"entry-content clearfix")]')
        vul_info = div.xpath('./div[2]//text()').extract()
        vul_info_list = [i.strip() for i in vul_info if i.strip()] + ['\n']
        vul_danger = div.xpath('./div[3]//text()').extract()
        vul_danger_list = [j.strip() for j in vul_danger if j.strip()] + ['\n']
        solution = div.xpath('./div[4]//text()').extract()
        solution_list = [z.strip() for z in solution if z.strip()] + ['\n']
        info_list = vul_info_list + vul_danger_list + solution_list
        info_str = item.get('cve') + '\n\n' + '\n'.join(info_list)
        item["detail_info"] = info_str
        print(item)
        yield item

