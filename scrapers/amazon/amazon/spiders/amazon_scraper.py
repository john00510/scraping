#coding: utf8
import scrapy, os
from com_functions import csv_opener, mongo_db
from functions import amazon_item_parser

class MySpider(scrapy.Spider):
    name = 'amazon'

    fh = csv_opener('amazon')
    client, coll = mongo_db()

    urls = open(os.path.abspath('scr_urls.txt'))

    def start_requests(self):
        count = 0
        for url in self.urls:
            count += 1
            print 'scraped: %s' % count
            yield scrapy.Request(
                url.strip(),
                headers={'referer': 'http://www.amazon.in/'},
                callback=self.parse
            )


    def parse(self, response):
        try:
            response.xpath('.//h1[@id="title"]/span/text()').extract()[0].strip()
            amazon_item_parser(response, self.fh, self.coll)
        except:
            print 'captcha error'
            yield scrapy.Request(
                response.url,
                headers={'referer': 'http://www.amazon.in/'},
                callback=self.parse,
                dont_filter=True
            )

