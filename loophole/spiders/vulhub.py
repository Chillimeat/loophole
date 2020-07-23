# -*- coding: utf-8 -*-
import scrapy
import re
import time
from urllib.parse import urljoin
from scrapy.http import Request
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class VulhubSpider(scrapy.Spider):
    name = 'vulhub'
    allowed_domains = ['vulhub.org.cn']
    start_urls = ['http://vulhub.org.cn/vulns']
    source = 'http://vulhub.org.cn'
    page = 1

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))
        item = RepositoryItem()
        tr_list_xpath = '//table/tbody/tr'
        tr_list = response.xpath(tr_list_xpath)
        for tr in tr_list:
            title = tr.xpath('./td[4]/text()').extract_first('').strip()
            cve = tr.xpath('./td[1]/a/text()').extract_first('').strip()
            if 'CVE' not in cve:
                continue
            link = tr.xpath('./td[1]/a/@href').extract_first('').strip()
            link = urljoin(self.source, link)
            date = tr.xpath('./td[2]/text()').extract_first('').strip()
            source = self.source
            item['title'] = title
            item['cve'] = cve
            item['link'] = link
            item['date'] = date
            item['source'] = source
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        # pattern = r'\d{0,9}'
        # total_number_text = response.xpath('//div[contains(@class,"bugs")]/div[2]/div/text()').extract()[-1].strip()
        # tmp_list = re.findall(pattern, total_number_text, re.I)
        # total_number = 0
        # for tmp in tmp_list:
        #     if tmp:
        #         total_number = int(tmp)
        # total_pages = total_number // 10 + 1
        # if self.page <= total_pages:
        self.page += 1
        if self.page <= TOTAL_PAGES:
            next_page_url = urljoin(self.start_urls[0] + '/', str(self.page))
            yield Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        cve = item.get('cve')
        description = response.xpath('//div[contains(@class,"col-md-9")]/div/p[1]/text()').extract_first("").strip()
        other_list = response.xpath('//div[@id="exploit-content"]/div//text()').extract()
        other_lst = [i.strip() for i in other_list if i.strip()]
        other_str = '\n'.join(other_lst)
        detail_info = cve + "\n\n" + description + '\n\n' + other_str
        item['detail_info'] = detail_info
        print(item)
        yield item




