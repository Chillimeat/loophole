# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymysql
import codecs
from loophole.settings import BASE_DIR


class LoopholePipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):
    def __init__(self):
        self.file_dir = os.path.join(BASE_DIR, 'savedata')
        self.file = None

    def process_item(self, item, spider):
        title = item["title"]
        date = item["date"]
        CVE = item["CVE"]
        source = item["source"]
        link = item["link"]
        name = spider.name
        self.file = codecs.open(os.path.join(self.file_dir, name + '.txt'), 'a+', encoding='utf-8')
        self.file.write(title + date + CVE + source + link + "\n")
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    def __init__(self, host, port, user, password, database, table):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            table=crawler.settings.get("MYSQL_TABLE"),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset="utf8", port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(["%s"] * len(data))
        sql_insert = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        sql_query = "select * from {} where title = '{}' and cve = '{}'".format(
            self.table,
            pymysql.escape_string(item['title']),
            pymysql.escape_string(item['cve'])
        )
        sql_create_table = """create table if not exists {} ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},{})""".format(
            self.table,
            'id int(11) AUTO_INCREMENT primary key',
            'download_id int(11)',
            'author varchar(50)',
            'type varchar(50)',
            'platform varchar(50)',
            'verified varchar(10)',
            'title varchar(255)',
            'date varchar(100)',
            'cve varchar(255)',
            'source varchar(255)',
            'link varchar(255)',
            'detail_info text',
        )
        try:
            if self.cursor.execute(sql_create_table):
                self.db.commit()
        except Exception as e:
            print(f'table exist: {e}')
        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
        except Exception as e:
            print(f'sql query error: {e}')
            result = ""
        if not result:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.db.commit()
        return item


class MysqlPipeline1(object):
    def __init__(self, host, port, user, password, database, table):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            table=crawler.settings.get("MYSQL_TABLE1"),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset="utf8", port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(["%s"] * len(data))
        sql_insert = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        sql_query = "select * from {} where title = '{}' and cve = '{}'".format(
            self.table,
            pymysql.escape_string(item['title']),
            pymysql.escape_string(item['cve'])
        )
        sql_create_table = """create table if not exists {} ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},{})""".format(
            self.table,
            'id int(11) AUTO_INCREMENT primary key',
            'download_id int(11)',
            'author varchar(50)',
            'type varchar(50)',
            'platform varchar(50)',
            'verified varchar(10)',
            'title varchar(255)',
            'date varchar(100)',
            'cve varchar(255)',
            'source varchar(255)',
            'link varchar(255)',
            'detail_info text',
        )
        try:
            if self.cursor.execute(sql_create_table):
                self.db.commit()
        except Exception as e:
            print(f'table exist: {e}')
        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
        except Exception as e:
            print(f'sql query error: {e}')
            result = ""
        if not result:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.db.commit()
        return item


