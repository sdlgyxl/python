#!/usr/bin/python3
#coding=utf-8
import datetime, time
from pymongo import MongoClient

class MongoNovel:
    mongoserver='122.14.220.20'
    mongoport = 27017

    def read(self, colls, query={}, fields={}, sortkey={}, limitnum=0):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        querystr='db.%s.find('%colls
        if len(query) > 0:
            querystr += str(query)
        if len(fields) > 0:
            querystr += ',' +str(fields) + ')'
        else:
            querystr += ')'
        if len(sortkey) > 0:
            querystr += '.sort(' + str(sortkey) + ')'
        if limitnum > 0:
            querystr += '.limit(' + str(limitnum) + ')'
        res = eval(querystr)
        client.close()
        return list(res)

    def test(self):
        client = MongoClient(self.mongoserver, self.mongoport)
        db = client.novel
        db.chapters.find({'bookname': '秦吏'},{'chapter': 1, 'no': 1, 'size': 1}).sort([("no",1)])
        client.close()
        
if __name__ == '__main__':
    mv = MongoNovel()
    #mv.test()
    
    books = mv.read('books')
    for x in books:
        size=0
        bookname=x['name']
        chapters = mv.read('chapters',{'bookname':bookname},{'chapter':1,'no':1, 'size':1, 'text':1},[('no',1)])
        path='e:\\temp\\%s.txt'%bookname
        f = open(path, 'w', encoding='utf-8')
        for each in chapters:
            size+=each['size']
            text = each.get('text', [])
            if len(text) > 0:
                f.write('\n'.join(text))
            else:
                print('error:', each)
        f.close()
        
    print('ok')        
