import scrapy
from com_functions import csv_opener, mongo_db
from functions import tatacliq_item_parser, tatacliq_items_parser
from urlparse import urljoin
from urls import urls


class MySpider9(scrapy.Spider):
    name = 'tatacliq9'
    allowed_domains = ['tatacliq.com']

    pgs = urls[8]['pages']
    url = urls[8]['url']
    itms = urls[8]['items']

    fh = csv_opener('tatacliq_kitchen_appliances')
    client, coll = mongo_db()

    def start_requests(self):
        for x in range(1, int(self.pgs)+1):
            #url = 'https://www.tatacliq.com/electronics-tablets/c-msh1211/page-%s' % x
            urll = self.url + '/page-%s' % x
            yield scrapy.Request(urll, callback=self.parse, headers={'referer': 'https://www.tatacliq.com'})

    def parse(self, response):
        items = response.xpath('.//li[@class="product-item"]')
        if len(items) == 0:
            pass
        for item in items:
            item_url = urljoin(response.url, item.xpath('.//h2/a/@href').extract()[0])
            price, offer_price, discount = tatacliq_items_parser(item)
            yield scrapy.Request(
                item_url, 
                meta={'price': price, 'offer_price': offer_price, 'discount': discount}, 
                callback=self.parse_items
            )

    def parse_items(self, response):
        tatacliq_item_parser(response, self.fh, self.coll)



