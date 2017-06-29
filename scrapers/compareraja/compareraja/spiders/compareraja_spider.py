import scrapy
from pymongo import MongoClient
import MySQLdb as mdb
from processors import scrape_item

class MySpider(scrapy.Spider):
    name = 'compareraja'

    def start_requests(self):
        client = MongoClient()
        db = client.stores
        coll1 = db['short_collection'].find({'source': 'compareraja.in'})
        total = coll1.count()

        conn = mdb.connect(
            host = '104.236.124.98',
            user = 'john',
            passwd = 'oWeiklxc',
            db = 'pricemer_db'
        )
        cur = conn.cursor()

        #cur.execute("TRUNCATE TABLE products")
        #cur.execute("TRUNCATE TABLE product_match")
        #cur.execute("TRUNCATE TABLE product_images")

        count = 0
        for c in coll1[:10]:
            url = c['url']
            cat = c['category']
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
                    'conn': conn,
                    'cur': cur,
                }
                )
            print 'total %s, scraped %s' % (total, count)

    def parse(self, response):
        scrape_item(response)

