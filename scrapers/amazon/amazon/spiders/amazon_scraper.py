import scrapy

class MySpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['http://www.amazon.in/gp/site-directory/ref=nav_shopall_btn']

    def start_requests(self):
        scrapy.Request(
            url = self.start_urls[0]
            headers = {'referer': 'http://www.amazon.in/'},
            callback = self.parse
        )

    def parse(self, response):
        pass
