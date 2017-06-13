import scrapy, os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tatacliq_spider import MySpider


log_file = '/'.join(os.path.abspath('').split('/')[:-3]) + '/logs/tatacliq.log'
if os.path.exists(log_file):
    os.remove(log_file)

process = CrawlerProcess(get_project_settings())
process.crawl(MySpider)
process.start()

