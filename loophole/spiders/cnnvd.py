# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from urllib.parse import urljoin
from copy import deepcopy
from loophole.items import RepositoryItem, YouRepositoryItem
from loophole.settings import SLEEP_TIME, TOTAL_PAGES


class CnnvdSpider(scrapy.Spider):
    name = 'cnnvd'
    allowed_domains = ['cnnvd.org.cn']
    source = 'http://www.cnnvd.org.cn'
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'loophole.pipelines.YouMysqlPipeline': 300,
        },
    }
    page = 1
    start_urls = ['http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno={}&repairLd='.format(page)]
    headers = {
        "Referer": 'http://www.cnnvd.org.cn'
    }

    def parse(self, response):
        print("==========当前抓取第{}页==========".format(self.page))

        item = YouRepositoryItem()
        total_pages = response.xpath('//div[@class="page"]/input[@id="pagecount"]/@value').extract_first(" ")
        li_list = response.xpath('//div[@class="list_list"]/ul/li')
        for li in li_list:
            title = li.xpath('./div/a/text()').extract_first(" ").strip()
            date_list = li.xpath('./div[2]/text()').extract()
            date = ''
            for date in date_list:
                if date:
                    date = date.strip()
                else:
                    date = ""
            link = li.xpath('./div/a/@href').extract_first(" ")
            link = urljoin(self.source, link)

            # # 我的
            # item["title"] = title
            # item["date"] = date
            # item["link"] = link
            # item["source"] = self.source
            # item["cve"] = ''
            # item['download_id'] = 0
            # item['type'] = ''
            # item['author'] = ''
            # item['platform'] = ''
            # item['verified'] = ''

            # you_sir的
            item['add_time'] = date

            yield Request(url=link, meta={"item": deepcopy(item)}, callback=self.detail_parse)
            time.sleep(SLEEP_TIME)

        self.page += 1
        next_url = urljoin(self.source, '/web/vulnerability/querylist.tag?pageno={}&repairLd='.format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, callback=self.parse, headers=self.headers)

    def detail_parse(self, response):
        item = response.meta.get("item")

        # # 我的
        # cve = response.xpath('//div[contains(@class,"detail_xq")]/ul/li[3]/a/text()').extract_first("").strip()
        # item["cve"] = cve
        # div = response.xpath('//div[contains(@class,"fl w770")]')
        # vul_profile = div.xpath('./div[3]//text()').extract()
        # vul_profile_list = [i.strip() for i in vul_profile if i.strip()] + ["\n"]
        # vul_announcement = div.xpath('./div[4]//text()').extract()
        # vul_announcement_list = [j.strip() for j in vul_announcement if j.strip()] + ["\n"]
        # references = div.xpath('./div[5]//text()').extract()
        # references_list = [z.strip() for z in references if z.strip()] + ["\n"]
        # effect = div.xpath('./div[6]//text()').extract()
        # effect_list = [x.strip() for x in effect if x.strip()] + ["\n"]
        # patch = div.xpath('./div[7]//text()').extract()
        # patch_list = [y.strip() for y in patch if y.strip()]
        # info_list = vul_profile_list + vul_announcement_list + references_list + effect_list + patch_list
        # info_str = cve + '\n\n' + '\n'.join(info_list)
        # item['detail_info'] = info_str

        # you_sir
        cve = response.xpath('//div[contains(@class,"detail_xq")]/ul/li[3]/a/text()').extract_first("").strip()
        item["name"] = cve
        div = response.xpath('//div[contains(@class,"fl w770")]')
        vul_profile = div.xpath('./div[3]//text()').extract()
        vul_profile_list = [i.strip() for i in vul_profile if i.strip()] + ["\n"]
        vul_announcement = div.xpath('./div[4]//text()').extract()
        vul_announcement_list = [j.strip() for j in vul_announcement if j.strip()] + ["\n"]
        references = div.xpath('./div[5]//text()').extract()
        references_list = [z.strip() for z in references if z.strip()] + ["\n"]
        effect = div.xpath('./div[6]//text()').extract()
        effect_list = [x.strip() for x in effect if x.strip()] + ["\n"]
        patch = div.xpath('./div[7]//text()').extract()
        patch_list = [y.strip() for y in patch if y.strip()]
        info_list = vul_profile_list + vul_announcement_list + references_list + effect_list + patch_list
        info_str = cve + '\n\n' + '\n'.join(info_list)
        item['urlinfo'] = info_str

        print(item)
        yield deepcopy(item)


