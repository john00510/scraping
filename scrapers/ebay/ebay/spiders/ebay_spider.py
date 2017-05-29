import scrapy, time, re
from ebay.functions import ebay_item_parser
from ebay.sel_spider import main
from ebay.com_functions import csv_opener


class MySpider(scrapy.Spider):
    name = 'ebay'
    start_urls = ['http://www.ebay.in']
    allowed_domains = ['http://www.ebay.in']

    l = main()
    fh = csv_opener('ebay')

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
        ebay_item_parser(response, self.fh, response.meta['category'])          



