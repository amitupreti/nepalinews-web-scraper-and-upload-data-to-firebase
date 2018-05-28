#verrsion 1 is the latest it srapes data real time when used with watch on linux  and uploads it to firebase server
# -*- coding: utf-8 -*-
#while dumping data use diffrent names according to the categories in the link
import scrapy
from scrapy import Selector
from scrapy import Request





#defining connection to firebase server
from firebase import firebase
firebase = firebase.FirebaseApplication('https://yourapplication.firebaseio.com/', None)
#please use the link to you firebase application


class OnlinekhabrSpider(scrapy.Spider):
    name = "onlinekhabr"

    #make changes to link here
    allowed_domains = ["onlinekhabar.com/content/news"]
    #start_urls = ('https://onlinekhabar.com/content/news/',)

    def __init__(self,address):
       
        self.start_urls = [address]

    def parse(self, response):
        
        links=response.xpath('//*[@class="news_loop"]/h2/a/@href').extract()
        for link in links:
            print(link)
            yield Request(link,callback= self.parse_article,dont_filter=True)

        
        nextpageurl = response.xpath('//*[@class="next page-numbers"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(nextpageurl)     
        yield scrapy.Request(absolute_next_page_url,dont_filter=True)




    def parse_article(self,response):
        title = response.xpath('//h1[@class="inside_head"]/text()').extract()
        title = title[0]
        article = response.xpath('//div[@class="ok-single-content"]/p/text()').extract()
        article = ''.join(article)

        

        #uploading to firebase server
        result = firebase.post('/Articles/', {'title': title,'news':article,'link':'onlikhabar'})

