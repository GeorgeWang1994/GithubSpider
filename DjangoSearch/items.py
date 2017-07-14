# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from enum import IntEnum


class ITEMTYPE(IntEnum):
    GitTagItem = 1,
    GitRepoItem = 2,
    GitUserItem = 3


# 标签
class GitTagItem(scrapy.Item):
    type = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()

    def detail(self):
        return "name: " + self.get('name')


# 分支
class GitRepoItem(scrapy.Item):
    type = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()
    lasttime = scrapy.Field()
    language = scrapy.Field()
    starnum = scrapy.Field()

    def detail(self):
        return "name: " + self.get('name') + "\nsummary: " + self.get('summary') + "\nstarnum: " + self.get('starnum')


# 用户
class GitUserItem(scrapy.Item):
    type = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    intro = scrapy.Field()
    avatar = scrapy.Field()
    location = scrapy.Field()
    email = scrapy.Field()

    def detail(self):
        return "name: " + self.get('name') + "\nintro" + self.get('intro')