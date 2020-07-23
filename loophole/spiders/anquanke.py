# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from copy import deepcopy
from urllib.parse import urljoin
from loophole.items import RepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class AnquankeSpider(scrapy.Spider):
    name = 'anquanke'
    allowed_domains = ['anquanke.com']
    source = 'https://www.anquanke.com'
    start_urls = ['https://www.anquanke.com/vul']
    page = 1
    headers = {
        'Referer': 'https://www.anquanke.com'
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))
        item = RepositoryItem()
        tr_list_xpath = '//div[@id="vul-list"]//table/tbody//tr'
        tr_list = response.xpath(tr_list_xpath)
        for tr in tr_list:
            link = tr.xpath('./td/div/a/@href').extract()
            title = tr.xpath('./td/div/a/text()').extract()
            update_date = tr.xpath('./td[5]/text()').extract()
            cve = tr.xpath('./td[2]//text()').extract()
            platform = [platform.strip() for platform in tr.xpath('./td[3]//text()').extract() if platform.strip()]
            item['link'] = urljoin(self.source, link[0])
            item['title'] = title[0].strip() if title else ''
            item['date'] = update_date[0].strip()
            item['cve'] = cve[0]
            item['source'] = self.source
            item['download_id'] = 0
            item['type'] = ''
            item['author'] = ''
            item['platform'] = platform[-1]
            item['verified'] = ''
            yield Request(url=item.get('link'), meta={'item': deepcopy(item)}, headers=self.headers, callback=self.parse_detail)
            time.sleep(SLEEP_TIME)

        self.page += 1
        total_pages = int(
            response.xpath('//*[@id="vul-list"]/nav/ul/li/a[text()="尾页"]/@href').extract_first('').split('=')[-1]
        )
        next_page_url = urljoin(self.source, "vul?page={}".format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_page_url, callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        item = response.meta.get('item')
        type = response.xpath('//table/tbody/tr[1]/td[4]/text()').extract_first("")
        item['type'] = type
        div = response.xpath('//div[contains(@class,"col-md-24")]')
        vul_sources = div.xpath('./div[2]//text()').extract()
        vul_sources_list = [i.strip() for i in vul_sources if i.strip()] + ["\n"]
        vul_detail = div.xpath('./div[3]//text()').extract()
        vul_detail_list = [j.strip() for j in vul_detail if j.strip()] + ["\n"]
        references = div.xpath('./div[4]//text()').extract()
        references_list = [z.strip() for z in references if z.strip()]
        info_list = vul_sources_list + vul_detail_list + references_list
        info_str = item['cve'] + '\n\n' + '\n'.join(info_list)
        item['detail_info'] = info_str
        print(item)
        yield deepcopy(item)


