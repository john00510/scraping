import scrapy
from pymongo import MongoClient
from processors import scrape_item, open_csv

class MySpider(scrapy.Spider):
    name = 'compareraja'


    def start_requests(self):
        client = MongoClient()
        db = client.stores
        coll1 = db['short_collection'].find({'source': 'compareraja.in'})
        total = coll1.count()
        coll2 = db['full_collection']
        fh = open_csv('compareraja')
        count = 0
        for c in coll1[:]:
            url = c['url']
            cat = c['category']
            src = c['source']
            name = c['name']
            count += 1
            yield scrapy.Request(
                url,
                callback = self.parse,
                headers = {
                    'referer': 'https://www.compareraja.in',
                },
                meta = {
                    'url': url,
                    'category': cat,
                    'name': name,
                    'source': src,
                    'coll': coll2,
                    'fh': fh,
                }
                )
            print 'total %s, scraped %s' % (total, count)

    def parse(self, response):
        scrape_item(response)

