import scrapy, os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from spiders.ebay_spider1 import MySpider1
from spiders.ebay_spider2 import MySpider2
from spiders.ebay_spider3 import MySpider3
from spiders.ebay_spider4 import MySpider4
from spiders.ebay_spider5 import MySpider5
from spiders.ebay_spider6 import MySpider6
from spiders.ebay_spider7 import MySpider7
from spiders.ebay_spider8 import MySpider8
from spiders.ebay_spider9 import MySpider9

log_file = '/'.join(os.path.abspath('').split('/')[:-3]) + '/logs/ebay.log'
if os.path.exists(log_file):
    os.remove(log_file)

process = CrawlerProcess(get_project_settings())
process.crawl(MySpider1)
process.crawl(MySpider2)
process.crawl(MySpider3)
process.crawl(MySpider4)
process.crawl(MySpider5)
process.crawl(MySpider6)
process.crawl(MySpider7)
process.crawl(MySpider8)
process.crawl(MySpider9)
process.start()

