# -*- coding: utf-8 -*-
import scrapy

class ChapterItem(scrapy.Item):
    bookname = scrapy.Field()
    chapter = scrapy.Field()
    url = scrapy.Field()
    is_fresh = scrapy.Field()
    size = scrapy.Field()
    no = scrapy.Field()
    down_date = scrapy.Field()
    text = scrapy.Field()


class BookItem(scrapy.Item):
    name = scrapy.Field()
    catalog_url = scrapy.Field()
    root_url = scrapy.Field()
    state = scrapy.Field()
    crdate = scrapy.Field()
哈哈哈
abcdefghi
123456789
