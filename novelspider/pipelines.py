# -*- coding: utf-8 -*-
import datetime
from pymongo import MongoClient
from novelspider.mongo import*

class MongoDBPipeline(object):
   def process_item(self, item, spider):        
        name = item.__class__.__name__
        if name == 'BookItem':
            MyMongo().delete_insert('books', {'name':item['name']}, dict(item))
            #MyMongo().insert('books', dict(item))
            #return '《%s》已经保存' % item('name')
        if name == 'ChapterItem':          
            MyMongo().update('chapters', {'url':item['url']}, dict(item))
            #return '《%s》-[%s]已经保存' % (item('bookname'), item('chapter'))

'''
def open_spider(self,spider):
    pass
def close_spider(self,spider):
    pass
'''