import scrapy
from functions import ebay_item_parser
from com_functions import mongo_open
from pymongo import MongoClient


class MySpider(scrapy.Spider):
    name = 'ebay'


    def start_requests(self):
        client = MongoClient()
        db = client.stores
        coll = db['short_collection']
        coll = coll.find({'source': 'ebay.in'})
        total = coll.count()
        count = 0

        client2, coll2 = mongo_open('full_collection')

        for c in coll:
            url = c['url']
            category = c['category']
            source = c['source']
            name = c['name']
            yield scrapy.Request(
                url, 
                callback=self.parse,  
                meta={
                    'category': category,
                    'name': name,
                    'source': source,
                    'url': url,
                    'coll': coll2,
                }
            )
            count += 1
            print 'total %s, scraped %s' % (total, count)

    def parse(self, response):
        ebay_item_parser(response)          

