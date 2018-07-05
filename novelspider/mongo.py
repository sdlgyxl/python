#!/usr/bin/python3
#coding=utf-8
import datetime, time
from pymongo import MongoClient
from novelspider.items import *

class MyMongo:
    mongoserver='122.14.220.20'
    mongoport = 27017

    #colls collections名称
    #item 字典类型
    def insert(self, colls, item):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db[colls].insert(item)
        client.close()

    #bookname string
    #page_chapters [[章节名称, zhangjie url,状态(0:不在数据库，1：在数据库,已下载，2：在数据库，未下载)]...]
    #update_no 是否修改全部no，0:不修改, 1:修改
    def save_page_chapters(self, bookname, page_chapters, update_no):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        colls = db.chapters
        for i in range(len(page_chapters)):
            each = page_chapters[i]
            #增加新章节
            if each[2] == 0:
                item= ChapterItem()
                item['bookname'] = bookname
                item['chapter'] = each[0]
                item['url'] = each[1]
                item['is_fresh'] = 1
                item['size'] = 0
                item['no'] = i + 1
                colls.insert_one(dict(item))
            #如果update_no == 1，则根据url修改章节顺序
            elif update_no == 1:
                colls.update({'url':each[1]},{'$set':{'no': i + 1}})
        client.close()

    def read(self, colls, query={}, fields={}, sortkey={}, limitnum=0):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        querystr='db[colls].find('
        if len(query) > 0:
            querystr += str(query)
        if len(fields) > 0:
            querystr += ',' + str(fields) + ')'
        else:
            querystr += ')'
        if len(sortkey) > 0:
            querystr += '.sort(' + str(sortkey) + ')'
        if limitnum > 0:
            querystr += '.limit(' + str(limitnum) + ')'
        res = eval(querystr)
        client.close()
        return list(res)

    def delete_insert(self, colls, filter, values):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        if db[colls].find(filter).count() > 0:
            db[colls].remove(filter)
        db[colls].insert_one(values)        
        client.close()

    def update(self, colls, filter, values):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db[colls].update(filter, {'$set':values})
        client.close()

    def clear_colls(self, colls):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db[colls].remove({})
        client.close()

    def remove_one_book(self, bookname):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db.chapters.remove({'bookname':bookname})
        db.books.remove({'name':bookname})
        client.close()

    def remove(self, colls, filter):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db[colls].remove(filter)
        client.close()
'''
#不包含 not like：  {url:{'$regex':'^((?!htt).)*$', '$options':'i'}}
if __name__ == '__main__':
    fi = {'url':{'$regex':'^((?!htt).)*$', '$options':'i'}}
    MyMongo().remove('chapters', fi)
    li=MyMongo().read('chapters', {'url':{'$regex':'^((?!htt).)*$', '$options':'i'}})
    for x in li:
        print(x)
        break
    input()
'''