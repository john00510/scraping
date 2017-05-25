import scrapy, sys
sys.path.append('/home/john/Scripts/upwork_projects/scraping/functions')
from functions import csv_opener, csv_writer
from tatacliq_functions import tatacliq_item_parser, tatacliq_items_parser
from urlparse import urljoin

class MySpider(scrapy.Spider):
    name = 'tatacliq'
    start_urls = ['https://www.tatacliq.com/electronics/c-msh12/']
    allowed_domains = ['tatacliq.com']

    fh = csv_opener('tatacliq')

    def parse(self, response):
        for x in range(1, 100):
            url = 'https://www.tatacliq.com/electronics/c-msh12/page-%s' % x
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        items = response.xpath('.//li[@class="product-item"]')
        if len(items) == 0:
            pass
        for item in items:
            item_url = response.urljoin(item.xpath('.//h2/a/@href').extract()[0])
            price, offer_price, discount = tatacliq_items_parser(item)
            yield scrapy.Request(
                item_url, 
                meta={'price': price, 'offer_price': offer_price, 'discount': discount}, 
                callback=self.parse_items
            )

    def parse_items(self, response):
        tatacliq_item_parser(response, self.fh)
 

    #fh.close()
