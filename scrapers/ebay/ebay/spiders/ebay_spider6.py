import scrapy, re
from functions import ebay_item_parser
from urls import urls
from com_functions import csv_opener, mongo_db


class MySpider6(scrapy.Spider):
    name = 'ebay6'
    allowed_domains = ['http://www.ebay.in']

    page1 = urls[5]['first_url']
    page2 = urls[5]['second_url']
    pgs = urls[5]['pages']
    category = urls[5]['cat_name']
    itms = 50

    fh = csv_opener('ebay_%s' % category.replace(' ', '_').lower())
    client, coll = mongo_db()

    def start_requests(self):
        yield scrapy.Request(
            self.page1, 
            headers={'referer': 'http://www.ebay.in'},
            callback=self.parse, 
            dont_filter=True, 
            meta={'category': self.category}
        )
        for x in range(2, self.pgs):
            url = re.sub(r'skc=50&', 'skc=%s&', re.sub(r'pgn=2&', 'pgn=%s&', self.page2) % x) % self.itms
            yield scrapy.Request(
                url, 
                headers={'referer': 'http://www.ebay.in'},
                callback=self.parse, 
                dont_filter=True, 
                meta={'category': self.category}
            )
            self.itms += 50

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



