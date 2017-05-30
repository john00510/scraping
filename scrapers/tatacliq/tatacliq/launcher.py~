import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tatacliq_spider1 import MySpider1
from spiders.tatacliq_spider2 import MySpider2

process = CrawlerProcess(get_project_settings())
process.crawl(MySpider1)
process.crawl(MySpider2)
process.start()

