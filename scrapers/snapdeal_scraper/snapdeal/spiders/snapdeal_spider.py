import scrapy, sys, os
sys.path.append('/'.join(os.path.abspath('').split('/')[:-3])+'/functions')
from functions import csv_opener, log_opener, log_writer
from snapdeal_functions import snapdeal_item_parser

class MySpider(scrapy.Spider):
    name = 'snapdeal'
    start_urls = ['https://www.snapdeal.com']

    fh = csv_opener('snapdeal')
    fh2 = log_opener('snapdeal')

    def parse(self, response):
        urls = [
            'https://www.snapdeal.com/product/jbl-t100a-in-ear-earphone/1808955798#bcrumbLabelId:288',
            'https://www.snapdeal.com/product/lyf-flame-8gb-black-grey/678753796085',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        try:
            snapdeal_item_parser(response, self.fh)
        except Exception, e:
            log_writer(self.fh2, response.url, e)

