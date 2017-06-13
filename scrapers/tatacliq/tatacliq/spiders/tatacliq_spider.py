import scrapy
from com_functions import csv_opener, mongo_db
from functions import tatacliq_item_parser, tatacliq_items_parser
from urlparse import urljoin
from urls import urls


class MySpider(scrapy.Spider):
    name = 'tatacliq'
    allowed_domains = ['tatacliq.com']

    fh = csv_opener('tatacliq')
    client, coll = mongo_db()

    def start_requests(self):
        for x in urls:
            pgs = x['pages']
            url = x['url']
            itms = x['items']
            for y in range(1, int(pgs)+1):
                #url = 'https://www.tatacliq.com/electronics-tablets/c-msh1211/page-%s' % x
                urll = url + '/page-%s' % y
                yield scrapy.Request(urll, callback=self.parse, headers={'referer': 'https://www.tatacliq.com'})

    def parse(self, response):
        items = response.xpath('.//li[@class="product-item"]')
        if len(items) == 0:
            pass
        for item in items:
            in_stock = item.xpath('.//a[@class="stockLevelStatus"]/text()').extract()
            item_url = urljoin(response.url, item.xpath('.//h2/a/@href').extract()[0])
            price, offer_price, discount = tatacliq_items_parser(item)
            yield scrapy.Request(
                item_url, 
                meta={
                    'price': price, 
                    'offer_price': offer_price, 
                    'discount': discount, 
                    'in_stock': in_stock
                }, 
                callback=self.parse_items
            )

    def parse_items(self, response):
        tatacliq_item_parser(response, self.fh, self.coll)



