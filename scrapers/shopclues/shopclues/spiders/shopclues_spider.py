import scrapy
from com_functions import csv_opener, mongo_db
from functions import shopclues_item_parser

class MySpider(scrapy.Spider):
    name = 'shopclues'

    fh = csv_opener('shopclues')
    client, coll = mongo_db()

    def start_requests(self):
        urls = [
            'http://www.shopclues.com/ivoomi-me1-5-inch-hd-ips-2gb-16gb-4g-volte-fast-charge-2.0.html',
            'http://www.shopclues.com/earth-black-zippo-type-lighter-selfie-stick-with-aux-cable.html',
            'http://www.shopclues.com/sketchfab-compact-pocket-size-selfie-stick-wired-for-iphone-and-android-black-119202709.html',
            'http://www.shopclues.com/ivoomi-iv-smart-4g-512mb-4gb-p-115023954.html',
            'http://www.shopclues.com/asus-zenfone-go-zb500kl-2gb-16gb-gold-118525792.html',
            'http://www.shopclues.com/zen-admire-joy-118295840.html',
        ]
        for url in urls:
            yield scrapy.Request(
                url, 
                headers={'referer': 'http://www.shopclues.com/'},
                callback=self.parse,
            )

    def parse(self, response):
        shopclues_item_parser(response, self.fh, self.coll)

