# -*- coding: utf-8 -*-
import scrapy
import os
import time
from scrapy.http import Request
from urllib.parse import urljoin
from copy import deepcopy

from loophole.items import RepositoryItem
from loophole.settings import BASE_DIR, SLEEP_TIME, TOTAL_PAGES


class PacketstormsecuritySpider(scrapy.Spider):
    name = 'packetstormsecurity'
    allowed_domains = ['packetstormsecurity.com']
    source = 'https://packetstormsecurity.com'
    start_urls = ['https://packetstormsecurity.com/files/']
    page = 1
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        "Referer": 'https://packetstormsecurity.com'
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))
        item = RepositoryItem()
        dl_list = response.xpath('//div[@id="m"]/dl')
        for dl in dl_list:
            title = dl.xpath('./dt/a/text()').extract_first("")
            link = dl.xpath('./dt/a/@href').extract_first("")
            link = urljoin(self.source, link)
            date = dl.xpath('./dd[@class="datetime"]/a/text()').extract_first("")
            source = self.source
            cve_list = dl.xpath('./dd[@class="cve"]/a//text()').extract()
            cve = ""
            tmp = []
            if cve_list:
                for cve in cve_list:
                    tmp.append(cve.strip())
                cve = ",".join(tmp)
                if len(cve) > 255:
                    cve = ",".join(tmp[:5]) + ",..."
            # download_link = dl.xpath('./dd[@class="act-links"]/a[1]/@href').extract_first("")
            # if download_link.split('.')[-1] != 'txt':
            #     continue
            # download_link = urljoin(self.source, download_link)
            # download_id = int(download_link.split('/')[-2])
            platform_list = dl.xpath('./dd[@class="os"]//a/text()').extract()
            platform = ','.join([i for i in platform_list if i])
            author_list = dl.xpath('./dd[@class="refer"]/a[@class="person"]/text()').extract()
            author = ','.join(author_list)
            item["title"] = title
            item["link"] = link
            item["source"] = source
            item["date"] = str(date)
            item["cve"] = cve
            # item['download_id'] = download_id
            item['type'] = ''
            item['author'] = author
            item['platform'] = platform
            item['verified'] = ''
            yield Request(url=link,
                          meta={'item': deepcopy(item)},
                          headers=self.headers,
                          callback=self.parse_detail,
                          )
            time.sleep(SLEEP_TIME)

        self.page += 1
        next_url = response.xpath('//div[@id="nv"]/a[text()="Next"]/@href').extract_first(" ")
        if next_url:
            next_url = urljoin(self.source, next_url)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url,
                          callback=self.parse,
                          headers=self.headers
                          )

    def parse_detail(self, response):
        item = response.meta.get('item')
        info_str = ''
        detail_info = response.xpath('//div[@id="m"]/div[@class="src"]/pre/code/text()').extract()
        for i in detail_info:
            info_str = info_str + i + '\n'
        # content = response.text
        # detail_info = content
        item['detail_info'] = info_str
        # download_id = item.get('download_id')
        # file_dir = os.path.join(BASE_DIR, 'download')
        # if not os.path.exists(file_dir):
        #     os.makedirs(file_dir)
        # with open(os.path.join(file_dir, '{}.txt'.format(download_id)), 'w+', encoding='utf-8') as f:
        #     f.write(content)
        print(item)
        yield item



