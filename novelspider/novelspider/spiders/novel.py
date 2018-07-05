# -*- coding: utf-8 -*-
# author: yangxiaolin
import scrapy, re, os, datetime
from novelspider.mongo import *
from novelspider.utility import *
from novelspider.items import *

class novelspider(scrapy.Spider):
    '''
    1、在init中，从数据库获取novel信息
    2、遍历novel目录（novel_catalogs），
            如果不在novel信息中，则写入数据库，并加入novel信息
    3、遍历novel信息， 下载目录页面
    4、分析目录页面，获得章节chapter信息（写入db））
    5、下载章节信息
    6、分析章节chapter信息
    7、把章节chapter信息写入本地文件

    '''
    name = "novel"
    allowed_domains = ["novel.com"]
    
    catalogs = ['https://www.23zw.me/olread/76/76441/index.html']
    
    def __init__(self):
        #self.books = MyMongo().read('books', {'name':'恶魔契约'})
        self.books = MyMongo().read('books')
        for each in self.books:
            for catalog in self.catalogs:
                if catalog.find(each['catalog_url']) > -1 or each['catalog_url'].find(catalog) > -1:
                    self.catalogs.remove(catalog)

    def start_requests(self):
        #增加新小说
        for catalog in self.catalogs:            
            yield scrapy.http.Request(url=catalog, callback=self.parse_newbook)
        #从数据库中获取小说，并检查更新
        for each in self.books:
            yield scrapy.http.Request(url=each['catalog_url'],
                callback=lambda response, book=each: self.parse_catalog(response, book),
                dont_filter=True)  
            

    #获取书名
    #检查book中是否已经存在该书名
    #如果没有书名，则增加
    #执行遍历
    def parse_newbook(self, response):
        book = MyUtility().get_bookinfo_from_catalog(response)  #return [name, catalog_url, root_url]
        if not book[0] in self.books:
            item = BookItem()
            item['name'] = book[0]
            item['catalog_url'] = book[1]
            item['root_url'] = book[2]
            item['state']=1
            item['crdate'] = datetime.datetime.utcnow()
            yield item
            dict_book=dict(item)
            yield scrapy.http.Request(url=response.url,
                callback=lambda response, book=dict_book: self.parse_catalog(response, book),
                dont_filter=True)  
    

    #分析目录页面，获得章节chapter信息（写入db））    
    def parse_catalog(self, response, book):
        #   获取书名        
        bookname = book['name']
        #   分析页面 获取章节
        book_root = book['root_url']
        #[[章节名称, zhangjie url,状态]...]
        page_chapters = MyUtility().get_page_chapters(response, book_root)
        #   提取数据库中已记录的章节
        db_chapters =  MyMongo().read('chapters', {'bookname':bookname},
                                    {'_id':1,'bookname':1,'chapter':1,'url':1,'is_fresh':1,'size':1,'down_date':1})
        #   把未记录的加入new_chaters
        #遍历页面章节目录
        update_no = 0
        for i in range(len(page_chapters)):
            for row in db_chapters: #检查数据库中章节
                if row['chapter'] == page_chapters[i][0]: #如果存在
                    if row.get('down_date') != None:
                        page_chapters[i][2] = 1
                    else:
                        page_chapters[i][2] = 2
                    if i + 1 != row.get('no', 0):
                        update_no = 1                    
                    break
        #保存页面的章节
        #   update_no==1 更改no
        #   page_chapters[i][2] == 0  增加记录
        #并提取应该下载的章节 down_date:null
        #保存页面的章节
        MyMongo().save_page_chapters(bookname, page_chapters, update_no)
        #对新章节和未下载章节进行下载
        for i in range(len(page_chapters)):
            item= ChapterItem()
            item['bookname'] = bookname
            item['chapter'] = page_chapters[i][0]
            item['url'] = page_chapters[i][1]
            item['is_fresh'] = 1
            item['no'] = i +1
            if page_chapters[i][2] != 1:
                #下载新章节
                yield scrapy.http.Request(url = item['url'], callback = lambda response, chapter = item: self.parse_chapter(response, chapter), dont_filter=True)


    #提取章节正文，并保存到数据库中
    def parse_chapter(self, response, chapter):
        if response.status >= 400:
            return
        
        #提取正文
        chapter['text'] = MyUtility().get_content(response)
        size=0
        for each in chapter['text']:
            size+=len(each)
        chapter['size'] = size
        chapter['down_date'] = datetime.datetime.utcnow()
        yield chapter
