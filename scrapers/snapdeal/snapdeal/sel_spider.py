from com_functions import firefox_spider
from selenium.webdriver.common.action_chains import ActionChains
import time, re
from sel_urls import urls
from pymongo import MongoClient


def hover(driver, element):
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()

def get_category(driver):
    category = driver.find_element_by_xpath('.//h1[@class="category-name"]').get_attribute('category').lower()
    if category == 'feature phone':
        category = 'mobile phones'
    return category

def error_func(driver):
    try:
        driver.find_element_by_xpath('.//div[@class="toptext letterSpace"]/span[contains(text(), "Internal Server Error")]')
    except:
        pass

def scroll_to_element(driver): 
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('.//div[@id="see-more-products"][contains(@style, "visible")]'))

def check_ip(url):
    driver = firefox_spider(url)
    time.sleep(10)
    driver.quit()

def scraping_cats(coll):
    for url in urls:
        scraping_cat(url, coll)

def items_found(driver):
    items = driver.find_elements_by_xpath('.//span[@class="totalCountHead"]/i')[1].get_attribute('innerHTML')
    return items

def scraping_cat(url, coll):
    driver = firefox_spider(url)
    #error_func(driver)
    total = items_found(driver)
    scraping_items(driver, coll, total)
    driver.quit() 

def scraping_items(driver, coll, total):
    l = []
    scrd = 0
    c = 0

    category = get_category(driver)
    while True:
        urls = driver.find_elements_by_xpath('.//section[@data-dpwlbl="Product Grid"]/div[contains(@class, "product-tuple-listing")]/div[contains(@class, "product-tuple-description")]/div[contains(@class, "product-desc-rating")]/a[@href]')
        urls = [(x.get_attribute('href'), category, 'snapdeal.com', x.find_element_by_xpath('./p').get_attribute('title')) for x in urls]
        if len(urls) == scrd:
            c += 1 
        l += urls
        l = list(set(l))
        print 'category: %s, total: %s, scraped: %s' % (category, total, len(urls))
        if int(total) == len(urls):
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            driver.find_element_by_xpath('.//div[@id="see-more-products"][contains(@style, "visible")]').click()
        except:
            pass
        scrd = len(urls)
        if c == 10:
            break     

    for el in l:
        d = {}
        d['url'], d['category'], d['source'], d['name'] = el
        coll.insert(d)

def main():
    client = MongoClient()
    db = client.stores
    coll = db['short_collection']
    scraping_cats(coll)
    client.close()

main()

