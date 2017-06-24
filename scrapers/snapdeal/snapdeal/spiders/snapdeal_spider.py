import scrapy, os
from pymongo import MongoClient
from functions import snapdeal_item_parser


class MySpider(scrapy.Spider):
    name = 'snapdeal'


    def start_requests(self):
        client = MongoClient()
        db = client.stores
        coll1 = db['short_collection']
        coll2 = db['full_collection']
        count = 0
        for x in coll1.find({'source': 'snapdeal.com'}):
            print 'scraped: %s' % count
            yield scrapy.Request(
                x['url'],
                headers={
                    'referer': 'https://www.snapdeal.com/',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
                },
                meta={
                    'source': x['source'],
                    'name': x['name'],
                    'category': x['category'],
                    'coll': coll2,
                }
                callback=self.parse
            )

    def parse(self, response):       
        snapdeal_item_parser(response)

