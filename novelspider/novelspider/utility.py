# -*- coding: utf-8 -*-
import os, re
from novelspider.items import *
get_site = lambda url : url.split('/')[2]
class MyUtility:
    #根据不同网站定义不同特征
    #title：目录页标题
    #bookname：目录页上的书名
    #root：章节根目录，与目录页上的章节地址合并成全地址
    #selchapter：根据css或xpath获取的章节列表，是selector
    #chapter：根据selchapter获取具体的章节名称和地址，是二维列表形式[[章节名称,章节地址]...]
    #content：章节页面上的章节正文
    #dirty：清理章节正文中的垃圾文本

    site_attrs = {'www.b5200.net':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'title[:title.index("无弹窗")]',
                                  'root':'catalog_url',
                                  'selchapter':'res.css("div#list dd")[9:]',
                                  'chapter':'self.extract_chapters_b5200(selchapters,book_root)',
                                  'content':'res.css("div#content p::text").extract()',
                                  'dirty':['\r\n', '\u3000\u3000\u3000\u3000']},
                  'www.23zw.me':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'title[:title.index(" ")]',
                                  'root':'catalog_url.replace("index.html", "")',
                                  'selchapter':'res.xpath(\'//div[@class="chapter_list_chapter"]\')',
                                  'chapter':'self.extract_chapters_23zw(selchapters,book_root)',
                                  'content':'res.css("div#text_area::text").extract()',
                                  'dirty':['8)', '\xa0\xa0\xa0']},
                  'www.biqugezw.com':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'res.css("h1::text").extract()[0]',
                                  'root':'str("https://www.biqugezw.com")',
                                  'selchapter':'res.xpath("//dd/a")',
                                  'chapter':'self.extract_chapters_biqugezw(selchapters,book_root)',
                                  'content':'res.css("div#content::text").extract()',
                                  'dirty':['\r\n', '一秒记住【笔趣阁中文网', '】，为您提供精彩小说阅读。', '手机用户请浏览m.biqugezw.com阅读，更优质的阅读体验。', '一秒记住【笔趣阁中文网】，为您提供精彩小说阅读。']},
                  'www.piaotian.com':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'res.css("h1::text").extract()[0][:-4]',
                                  'root':'res.url',
                                  'selchapter':'res.css("li")',
                                  'chapter':'self.extract_chapters_piaotian(selchapters,book_root)',
                                  'content':'res.css("body::text").extract()',
                                  'dirty':['\r\n', '最新最快更新，提供免费阅读']},
                  'www.ranwena.com':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'res.css("h1::text").extract()[0]',
                                  'root':'str("")',
                                  'selchapter':'res.css("div.box_con dd")',
                                  'chapter':'self.extract_chapters_b5200(selchapters,book_root)',
                                  'content':'res.css("div#content::text").extract()',
                                  'dirty':[]},
                  'www.banfusheng.com':{'title':'res.css("title::text").extract()[0]',
                                  'bookname':'title.partition("无弹窗")[0]',
                                  'root':'str("http://www.banfusheng.com")',
                                  'selchapter':'res.css("div.chapter-list li")',
                                  'chapter':'self.extract_chapters_b5200(selchapters,book_root)',
                                  'content':'res.css("div#content p::text").extract()',
                                  'dirty':[]
                                  }
                  }
    #从目录页获取小说信息
    def get_bookinfo_from_catalog(self, res):
        site = get_site(res.url)
        attr = self.site_attrs[site]
        title = eval(attr['title'])
        name = eval(attr['bookname'])
        catalog_url = res.url
        root_url = eval(attr['root'])
        return [name, catalog_url, root_url]

    #整理书名 章节名， 只留下中英文数字，删除[]*@#等
    def pretty_name(self, name):
        pattern = '[\u4e00-\u9fff\w\d]+'  # 汉字正则表达式
        re_compile = re.compile(pattern)
        res = re_compile.findall(name.strip().replace(' ', '-'))
        tmp = ""
        for g in res:
            tmp += g
        
        return tmp

    #生成章节全地址
    def join(self, root, url):
        if url[:4].lower() == 'http':
            return url
        return root + url

    #判断章节名称是否已经存在
    def is_exist(self, text, list):
        for each in list:
            if text in each:
                return True
        return False

    #分析飘天的章节
    def extract_chapters_piaotian(self, sels, book_root):
        if sels[0].xpath('a/text()').extract()[0] == '添加到IE收藏夹':
            sels = sels[4:]
        chapters = []
        for sel in sels:
            if len(sel.css('a')) == 0:
                break

            text = self.pretty_name(sel.xpath('a/text()').extract()[0])
            href = self.join(book_root, sel.xpath('a/@href').extract()[0])
            if self.is_exist(text, chapters) == False:
                chapters.append([text, href, 0])        
        return chapters      

    #分析笔趣阁中文的章节
    def extract_chapters_biqugezw(self, sels, book_root):
        chapters = []
        for sel in sels:
            text = self.pretty_name(sel.xpath('text()').extract()[0])
            href = self.join(book_root, sel.xpath('@href').extract()[0])
            if self.is_exist(text, chapters) == False:
                try:
                    chapters.append([text, href, 0])        
                except:
                    print("error=", book_root)
        return chapters

    #分析b5200的章节，燃文、半浮生通用
    def extract_chapters_b5200(self, sels, book_root):
        chapters = []
        for sel in sels:
            try:
                text = self.pretty_name(sel.xpath('a/text()').extract()[0])
                href = self.join(book_root, sel.xpath('a/@href').extract()[0])
                if self.is_exist(text, chapters) == False:
                    chapters.append([text, href, 0])
            except:
                continue
        return chapters  

    #分析傲世中文的章节
    def extract_chapters_23zw(self, sels, book_root):
        chapters=[[]] * (len(sels) *2 + 10)
        index = 0
        for sel in sels:
            row = int(index / 4)
            col = index % 4
            index += 1
            text =  sel.xpath('a/text()').extract()
            href = sel.xpath('a/@href').extract()
            for i in range(len(text)):
                if self.is_exist(text[i], chapters) == False:
                    chapters[row * 8 + i * 4 + col] = [self.pretty_name(text[i]), self.join(book_root, href[i]), 0]
        while [] in chapters:
            chapters.remove([])
        return chapters

    #返回列表，[[章节名称, 章节url,状态]...]
    def get_page_chapters(self, res, book_root):
        site = get_site(res.url)
        attr = self.site_attrs[site]
        selchapters = eval(attr['selchapter'])
        chapters = eval(attr['chapter'])
        return chapters

    #清洗正文，删除垃圾文本
    def clean_up(self, lines, dirty):   
        for i in range(len(lines)):
            for d in dirty:
                if lines[i].find(d) != -1:
                    lines[i] = lines[i].replace(d, '')
            if len(lines[i]) > 4:
                lines[i] += '\r'

        return lines

    #获取章节正文
    def get_content(self, res):
        site = get_site(res.url)
        attr = self.site_attrs[site]
        content = eval(attr['content'])
        dirty  = attr['dirty']
        if len(dirty) > 0:
            content = self.clean_up(content, dirty)
        return content
