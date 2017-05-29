import scrapy
from com_functions import csv_opener
from functions import tatacliq_item_parser, tatacliq_items_parser
from urlparse import urljoin


class MySpider1(scrapy.Spider):
    name = 'tatacliq1'
    allowed_domains = ['tatacliq.com']

    fh = csv_opener('tatacliq_tablets')

    def start_requests(self):
        for x in range(1, 15):
            #url = 'https://www.tatacliq.com/electronics/c-msh12/page-%s' % x
            url = 'https://www.tatacliq.com/electronics-tablets/c-msh1211/page-%s' % x
            yield scrapy.Request(url, callback=self.parse, headers={'referer': 'https://www.tatacliq.com'})

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
        tatacliq_item_parser(response, self.fh)



