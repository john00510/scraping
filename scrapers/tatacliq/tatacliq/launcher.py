import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
from scrapy.utils.log import configure_logging
from spiders.tatacliq_spider1 import MySpider1
from spiders.tatacliq_spider2 import MySpider2
from spiders.tatacliq_spider3 import MySpider3
from spiders.tatacliq_spider4 import MySpider4
from spiders.tatacliq_spider5 import MySpider5
from spiders.tatacliq_spider6 import MySpider6
from spiders.tatacliq_spider7 import MySpider7
from spiders.tatacliq_spider8 import MySpider8
from spiders.tatacliq_spider9 import MySpider9
from spiders.tatacliq_spider10 import MySpider10
from spiders.tatacliq_spider11 import MySpider11
from spiders.tatacliq_spider12 import MySpider12
from spiders.tatacliq_spider13 import MySpider13

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename = 'tatacliq.log',
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
process.crawl(MySpider11)
process.crawl(MySpider12)
process.crawl(MySpider13)
process.start()

