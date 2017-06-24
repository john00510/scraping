from processors import chrome_spider
from selenium.webdriver.common.keys import Keys
from cat_urls import urls
from pymongo import MongoClient
import time


def get_category(coll):
    for url in urls:
        category = url['category']
        url = url['url']
        driver = chrome_spider(url)
        get_items(driver, coll, category)
        driver.quit()

def get_items(driver, coll, category):
    current = None
    while True:
        past = current
        scroll_down(driver)
        pages = driver.find_elements_by_xpath('.//div[@class="prodcut-listing"]/form[@id="form1"]')
        current = len(pages)
        print 'category: %s, page: %s' % (category, current)
        if current == past:
            parse_items(driver, coll, category)
            driver.quit()
            break
        time.sleep(5)

def parse_items(driver, coll, category):
    items1 = driver.find_elements_by_xpath('.//div[@class="prodcut-listing"]/ul')
    for item in items1:
        d = {}
        d['name'] = item.find_element_by_xpath('.//a[@class="db"]').get_attribute('title')
        d['category'] = category
        d['url'] = item.find_element_by_xpath('.//a[@class="db"]').get_attribute('href')
        d['source'] = 'compareraja.in'
        coll.insert(d)

    items2 = driver.find_elements_by_xpath('.//div[@class="prodcut-listing"]/form[@id="form1"]/ul')
    for item in items2:
        d2 = {}
        d2['name'] = item.find_element_by_xpath('.//a[@class="db"]').get_attribute('title')
        d2['category'] = category
        d2['url'] = item.find_element_by_xpath('.//a[@class="db"]').get_attribute('href')
        d2['source'] = 'compareraja.in'
        coll.insert(d2)

def scroll_down(driver):
    count = 0
    while True:
        try:
            driver.find_element_by_xpath('.//a[@title="Show more results"]').click()
            break
        except:
            driver.find_element_by_xpath('.//body').send_keys(Keys.ARROW_DOWN)
            count += 1
            if count == 10:
                break
            time.sleep(0.2)


if __name__ == '__main__':
    client = MongoClient()
    db = client.stores
    coll = db['short_collection']
    get_category(coll)
    client.close()


