import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
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
from spiders.ebay_spider10 import MySpider10

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename = 'ebay.log',
    filemode = 'w',
    format = '%(levelname)s: %(message)s',
    level = logging.ERROR
)

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
process.crawl(MySpider10)
process.start()

