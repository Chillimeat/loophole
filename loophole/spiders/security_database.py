# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from selenium import webdriver
from urllib.parse import urljoin
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import CHROME_SERVICE_ARGS, CHROME_DIR, SLEEP_TIME, TOTAL_PAGES


class SecurityDatabaseSpider(scrapy.Spider):
    name = 'security-database'
    allowed_domains = ['security-database.com']
    source = 'http://www.security-database.com'
    # custom_settings = {
    #     # 设置管道下载
    #     'ITEM_PIPELINES': {
    #         'loophole.pipelines.MysqlPipeline': 300,
    #     },
    #     # 设置log日志
    #     'LOG_LEVEL': 'DEBUG',
    # }
    page = 1
    base_url = 'http://www.security-database.com/view-all.php?page={}&type=cve'
    begin_url = base_url.format(page)
    # headers = {
    #     "Referer": 'http://www.security-database.com'
    # }

    def __init__(self):
        super(SecurityDatabaseSpider, self).__init__(name='security-database')
        self.timeout = 20
        options = webdriver.ChromeOptions()
        options.binary_location = CHROME_DIR
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            executable_path=CHROME_SERVICE_ARGS,
            chrome_options=options,
        )
        self.driver.maximize_window()
        # self.driver.set_page_load_timeout(self.timeout)

    def start_requests(self):
        yield Request(url=self.begin_url, callback=self.parse)

    def parse(self, response):
        print("==========当前正在获取第{}页==========".format(self.page))
        item = RepositoryItem()
        tr_list = response.xpath('//div[@id="primary"]/table[2]//tr')
        for tr in tr_list[1:]:
            date = tr.xpath('./td[2]/text()').extract_first("")
            cve = tr.xpath('./td[3]/b/a/text()').extract_first("")
            link = tr.xpath('./td[3]/b/a/@href').extract_first("")
            link = urljoin(self.source, link)
            title = tr.xpath('./td[5]/text()').extract_first("")
            source = self.source
            item["cve"] = cve
            item["date"] = date
            item["link"] = link
            item["title"] = title
            item["source"] = source
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, callback=self.parse_detail)

        # total_counts = response.xpath(
        #     '//div[@id="primary"]/table[3]//tr/td[2]/text()').extract_first("").split(":")[-1].strip()
        # print(self.page, ':', total_counts)
        # total_pages = int(total_counts) // 20 + 1 if total_counts else self.page
        self.page += 1
        next_url = self.base_url.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        cve = item.get('cve')
        detail_name = response.xpath('//div[@id="primary"]/h3[3]/text()').extract_first("")
        detail_value = response.xpath('//div[@id="primary"]/table[3]//text()').extract_first("")
        original_source_name = response.xpath('//div[@id="primary"]/h3[4]/text()').extract_first("")
        original_source_value = 'Url:' + response.xpath('//div[@id="primary"]/table[4]/tbody/tr/td/a/text()').extract_first("")
        source_detail_name = response.xpath('//div[@id="primary"]/h3[5]/text()').extract_first("")
        source_detail_value_list = []
        tr_list = response.xpath('//div[@id="primary"]/table[5]/tbody/tr')
        for tr in tr_list[1:]:
            source = 'Source: ' + tr.xpath('//div[@id="primary"]/table[5]/tbody/tr[2]/td[1]/text()').extract_first("")
            url_list = tr.xpath('//div[@id="primary"]/table[5]/tbody/tr[2]/td[2]/a/text()').extract()
            url = 'Url: ' + ','.join(url_list)
            source_detail_value_list.append(source)
            source_detail_value_list.append(url)
        source_detail_value = '\n'.join(source_detail_value_list)
        detail_info = cve + "\n\n" + detail_name + "\n" + detail_value + "\n\n" + original_source_name + "\n" + original_source_value + "\n\n" + source_detail_name + '\n' + source_detail_value
        item['detail_info'] = detail_info
        print(item)
        yield item



