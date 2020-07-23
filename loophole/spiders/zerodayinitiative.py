# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urljoin
from selenium import webdriver
from copy import deepcopy
from loophole.items import RepositoryItem
from loophole.settings import CHROME_SERVICE_ARGS, CHROME_DIR


class ZerodayinitiativeSpider(scrapy.Spider):
    name = 'zerodayinitiative'
    allowed_domains = ['zerodayinitiative.com']
    source = 'https://www.zerodayinitiative.com'
    base_url = 'https://www.zerodayinitiative.com/advisories/published/'
    page = 1
    headers = {
        'Referer': 'https://www.zerodayinitiative.com'
    }

    def __init__(self):
        super(ZerodayinitiativeSpider, self).__init__(name='zerodayinitiative')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.binary_location = CHROME_DIR
        self.driver = webdriver.Chrome(
            executable_path=CHROME_SERVICE_ARGS,
            chrome_options=options
        )
        self.driver.maximize_window()

    def start_requests(self):
        yield Request(url=self.base_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        print("==========当前正在获取第{}页==========".format(self.page))
        item = RepositoryItem()
        tr_list = response.xpath('//table[@id="publishedAdvisories"]//tr')
        for tr in tr_list:
            cve = tr.xpath('./td[4]/text()').extract_first("")
            if not cve:
                continue
            publish_date = tr.xpath('./td[5]/text()').extract_first("")
            title = tr.xpath('./td[7]/a/text()').extract_first("")
            link = tr.xpath('./td[7]/a/@href').extract_first("")
            link = urljoin(self.source, link)
            source = self.source
            item["cve"] = cve
            item["date"] = publish_date
            item["title"] = title
            item["link"] = link
            item["source"] = source
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = ''
            item['verified'] = ''
            yield Request(url=link, meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta.get('item')
        cve = item.get('cve')
        info_list = []
        tr_list = response.xpath('//div[contains(@class,"advisories-details")]/table/tbody/tr')
        for tr in tr_list:
            name = tr.xpath('./td[1]/text()').extract_first("")
            value_list = tr.xpath('./td[2]//text()').extract()
            value_lst = [i.strip() for i in value_list if i.strip()]
            value = '\n'.join(value_lst)
            info_list.append('{}          {}'.format(name, value))
        info_str = cve + '\n\n' + '\n'.join(info_list)
        item['detail_info'] = info_str
        print(item)
        yield item
