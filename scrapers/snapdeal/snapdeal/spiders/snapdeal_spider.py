import scrapy, os
from com_functions import csv_opener, mongo_db
from functions import snapdeal_item_parser


class MySpider(scrapy.Spider):
    name = 'snapdeal'

    fh = csv_opener('snapdeal')
    client, coll = mongo_db()

    urls = open(os.path.abspath('scr_urls.txt'))

    def start_requests(self):
        count = 0
        for url in self.urls:
            count += 1
            print 'scraped: %s' % count
            yield scrapy.Request(
                url.strip(),
                headers={'referer': 'https://www.snapdeal.com/'},
                callback=self.parse_page
            )

    def parse_page(self, response):       
        snapdeal_item_parser(response, self.fh, self.coll)

