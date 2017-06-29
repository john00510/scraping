from processors import chrome_spider
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from cat_urls import urls
import time


def get_category(coll):
    for url in urls:
        driver = chrome_spider(url)
        get_items(driver, coll)
        driver.quit()

def get_items(driver, coll):
    current = None
    while True:
        past = current
        scroll_down(driver)
        time.sleep(5)
        items = driver.find_elements_by_xpath('.//li[@class="product-item"]')
        current = len(items)
        print 'current %s, past %s' % (current, past)
        if current == past:
            parse_items(driver, coll)
            driver.quit()
            break

def parse_items(driver, coll):
    items = driver.find_elements_by_xpath('.//li[@class="product-item"]')
    for item in items:
        d = {}
        d['url'] = item.find_element_by_xpath('.//h2/a').get_attribute('href')
        d['name'] = item.find_element_by_xpath('.//div[@class="image"]/a').get_attribute('title')
        d['source'] = 'tatacliq.com'
        coll.insert(d)
    print 'scraped % items' % len(items)

def scroll_down(driver):
    count = 0
    while True:
        try:
            driver.find_element_by_xpath('.//button[@class="loadMorePageButton"]').click()
            break
        except:
            driver.find_element_by_xpath('.//body').send_keys(Keys.ARROW_DOWN)
            count += 1
            if count == 300:
                break
            time.sleep(0.5)


if __name__ == '__main__':
    client = MongoClient()
    db = client.stores
    coll = db['short_collection']
    get_category(coll)
    client.close()


