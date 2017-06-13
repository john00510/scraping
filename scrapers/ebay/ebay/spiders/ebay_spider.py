import scrapy, re
from functions import ebay_item_parser
from urls import urls
from com_functions import csv_opener, mongo_db


class MySpider(scrapy.Spider):
    name = 'ebay'
    allowed_domains = ['http://www.ebay.in']

    fh = csv_opener('ebay')
    client, coll = mongo_db()

    def start_requests(self):
        for x in urls:
            page1 = x['first_url']
            page2 = x['second_url']
            pgs = x['pages']
            category = x['cat_name']
            itms = 50
            yield scrapy.Request(
                page1, 
                headers={'referer': 'http://www.ebay.in'},
                callback=self.parse, 
                dont_filter=True, 
                meta={'category': category}
            )
            for y in range(2, pgs):
                url = re.sub(r'skc=50&', 'skc=%s&', re.sub(r'pgn=2&', 'pgn=%s&', page2) % x) % itms
                yield scrapy.Request(
                    url, 
                    headers={'referer': 'http://www.ebay.in'},
                    callback=self.parse, 
                    dont_filter=True, 
                    meta={'category': category}
                )
                itms += 50

    def parse(self, response):
        urls = response.xpath('.//ul[@id="ListViewInner"]/li/h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(
                url, 
                callback=self.parse_pages, 
                dont_filter=True, 
                meta={'category': response.meta['category']}
            )

    def parse_pages(self, response):
        ebay_item_parser(response, self.fh, response.meta['category'], self.coll)          



