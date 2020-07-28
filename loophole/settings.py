# -*- coding: utf-8 -*-

# Scrapy settings for loophole project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys

BOT_NAME = 'loophole'

SPIDER_MODULES = ['loophole.spiders']
NEWSPIDER_MODULE = 'loophole.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'loophole (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'loophole.middlewares.LoopholeSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'loophole.middlewares.LoopholeDownloaderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
    'loophole.middlewares.RandomUserAgentMiddleware': 543,
    'loophole.middlewares.SeleniumMiddleware': 600,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'loophole.pipelines.LoopholePipeline': 300,
# }
ITEM_PIPELINES = {
    'loophole.pipelines.MysqlPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set url max length size
URLLENGTH_LIMIT = 5000

# mysql database config
MYSQL_HOST = '127.0.0.1'
YOU_MYSQL_HOST = '192.168.0.130'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'spider'
YOU_MYSQL_DATABASE = 'gcdb'
MYSQL_TABLE = 'vul_info'
YOU_MYSQL_TABLE = 'bug_cve'
EXPLOIT_DB_MYSQL_TABLE = 'bug_expdb'
MYSQL_TABLE1 = 'vul_info1'

# set proxy
# 如：'http://180.125.196.155:8888'
PROXY = ''

# set selenium middleware
SELENIUM_TIMEOUT = 20
CHROME_SERVICE_ARGS = os.path.join(BASE_DIR,
                                   'utils',
                                   'chromedriver',
                                   'win-chrome',
                                   'chromedriver.exe') if 'win' in sys.platform else os.path.join(BASE_DIR,
                                                                                                  'utils',
                                                                                                  'chromedriver',
                                                                                                  'linux-chrome',
                                                                                                  'chromedriver')
CHROME_DIR = os.path.join(BASE_DIR, 'utils', 'Chrome', 'Application', 'chrome.exe')

# set spider sleep time
SLEEP_TIME = 1

# set list page numbers
TOTAL_PAGES = 10

# 增加并发：
# 默认scrapy开启的并发线程为32个，可以适当进行增加。
# 在settings配置文件中修改CONCURRENT_REQUESTS = 100值为100,并发设置成了为100
# CONCURRENT_REQUESTS = 32

# 禁止cookie：
# 如果不是真的需要cookie，则在scrapy爬取数据时可以进制cookie从而减少CPU的使用率，提升爬取效率。
COOKIES_ENABLED = False

# 禁止重试：
# 对失败的HTTP进行重新请求（重试）会减慢爬取速度，因此可以禁止重试。
# RETRY_ENABLED = False

# 减少下载超时：
# 如果对一个非常慢的链接进行爬取，减少下载超时可以能让卡住的链接快速被放弃，从而提升效率。
# DOWNLOAD_TIMEOUT = 10

# 降低日志级别：
# 在运行scrapy时，会有大量日志信息的输出，为了减少CPU的使用率。
LOG_LEVEL = 'INFO'  # 指定日志信息种类
# LOG_LEVEL = 'DEBUG'
# LOG_FILE = os.path.join(BASE_DIR, 'log.txt')  # 表示将日志信息写到指定的文件中进行存储


