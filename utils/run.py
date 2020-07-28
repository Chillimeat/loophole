from scrapy.cmdline import execute
import os
import sys
from loguru import logger

command_list = [
                # "scrapy crawl anquanke",
                # "scrapy crawl cnnvd",
                "scrapy crawl exploit_db",

                # "scrapy crawl cxsecurity",
                # "scrapy crawl daybank",
                # "scrapy crawl nsfocus",
                # "scrapy crawl packetstormsecurity",
                # "scrapy crawl rapid7",
                # "scrapy crawl vulhub",
                # "scrapy crawl winicssec",
                # "scrapy crawl security-database",
                # "scrapy crawl zerodayinitiative",
                ]
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run():
    # 通用的方法，但是一次只能执行一个spider
    # execute(['scrapy', 'crawl', 'rapid7'])
    # os.system("scrapy crawl spider")方法：可以灵活执行多个，并设置时间等

    # for command in command_list:
    #     os.system(command)
    #     os.system(command + "-s CLOSESPIDER_TIMEOUT=3600")  # 每一个爬虫设置一个定时器，让每一个爬虫爬取一段时间，再运行下一个爬虫即可

    for command in command_list:
        try:
            os.system(command)
        except Exception as e:
            logger.exception(f'{e}')
            logger.info(f'运行爬虫脚本{command}异常')


if __name__ == '__main__':
    run()




