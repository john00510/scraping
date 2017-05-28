import scrapy, sys, os
sys.path.append('/'.join(os.path.abspath('').split('/')[:-3])+'/functions')
from functions import csv_opener, csv_writer, log_opener, log_writer
from shopclues_functions import shopclues_item_parser

class MySpider(scrapy.Spider):
    name = 'shopclues'
    allowed_domains = ['www.shopclues.com']
    start_urls = ['http://www.shopclues.com']

    fh = csv_opener('shopclues')
    fh2 = log_opener('shopclues')

    def parse(self, response):
        urls = [
            'http://www.shopclues.com/ivoomi-me1-5-inch-hd-ips-2gb-16gb-4g-volte-fast-charge-2.0.html',
            'http://www.shopclues.com/earth-black-zippo-type-lighter-selfie-stick-with-aux-cable.html',
            'http://www.shopclues.com/sketchfab-compact-pocket-size-selfie-stick-wired-for-iphone-and-android-black-119202709.html',
            'http://www.shopclues.com/ivoomi-iv-smart-4g-512mb-4gb-p-115023954.html',
            'http://www.shopclues.com/asus-zenfone-go-zb500kl-2gb-16gb-gold-118525792.html',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        try:
            shopclues_item_parser(response, self.fh)
        except Exception, e:
            log_writer(self.fh2, response.url, e)

