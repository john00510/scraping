import scrapy, sys, time, re, os
sys.path.append('/'.join(os.path.abspath('').split('/')[:-3])+'/functions')
from ebay_functions import main, ebay_item_parser
from functions import csv_opener, csv_writer, log_opener, log_writer


class MySpider(scrapy.Spider):
    name = 'ebay'
    start_urls = ['http://www.ebay.in']
    allowed_domains = ['http://www.ebay.in']

    l = main()
    fh = csv_opener('ebay')
    fh2 = log_opener('ebay')

    def parse(self, response):
        for cat in self.l:
            pg = 2
            itms = 50
            page1 = cat[0]
            page2 = cat[1]
            category = cat[-1]
            yield scrapy.Request(page1, callback=self.parse_pages, dont_filter=True, meta={'category': category})
            while True:
                url = re.sub(r'skc=50&', 'skc=%s&', re.sub(r'pgn=2&', 'pgn=%s&', page2) % pg) % itms
                yield scrapy.Request(url, callback=self.parse_pages, dont_filter=True, meta={'category': category})
                if pg == 20: break
                pg += 1
                itms += 50
                time.sleep(2)

    def parse_pages(self, response):
        urls = response.xpath('.//ul[@id="ListViewInner"]/li/h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page, dont_filter=True, meta={'category': response.meta['category']})

    def parse_page(self, response):
        try:
            ebay_item_parser(response, self.fh, response.meta['category'])
        except Exception, e:
            log_writer(self.fh2, response.url, e)            



