#encoding: utf8
from com_functions import mongo_open, mongo_write, spider
from groups import groups
import time, re


def total_count(driver):
    tc = driver.find_element_by_xpath('.//h2[@id="s-result-count"]').text
    try:
        return re.findall(r' ([0-9,.]+) ', tc)[0].replace(',', '')
    except:
        return re.findall(r'^([0-9]+) ', tc)[0]

def mobile_exc(driver):
    try:
        driver.find_element_by_xpath('.//span[contains(text(), "Basic Mobiles")]').click()
        time.sleep(5)
        return driver
    except:
        print 'mobile exception error'

def brand_func(item):
    try:
        return item.find_element_by_xpath('.//span[contains(text(), "by")]/following-sibling::span').text.strip().lower()
    except:
        return 'uknown'

def scraping_cats(url):
    driver = spider(url)
    time.sleep(5)
    cats = driver.find_element_by_xpath('.//table[@id="shopAllLinks"]')
    cats = cats.find_elements_by_xpath('.//li/a[@href]')
    urls = []
    for cat in cats:
        d = {}
        d['cat_name'] = cat.text.strip()
        if len(d['cat_name']) == 0:
            continue
        if d['cat_name'] not in groups:
            continue
        d['url'] = cat.get_attribute('href')
        urls.append(d)

    driver.quit()
    print 'scraped %s categories' % (len(urls))
    return urls

def scraping_cat(urls, coll):
    for u in urls:+

        url = u['url']
        cat_name = u['cat_name'].lower()
        driver = spider(url)
        if cat_name == 'all mobile phones':
            driver = mobile_exc(driver)
        total = total_count(driver)
        scraped = 0

        while True:
            items = driver.find_elements_by_xpath('.//div[@id="mainResults"]/ul/li[@data-asin]')
            if len(items) == 0:
                items = driver.find_elements_by_xpath('.//ul[@id="s-results-list-atf"]/li[@data-asin]')
            scraped += len(items)
            print '%s, total: %s, scraped: %s' % (cat_name, total, scraped)
            for item in items:
                d = {}
                d['url'] = item.find_element_by_xpath('.//a[@title]').get_attribute('href').strip()
                d['name'] = item.find_element_by_xpath('.//a[@title]').get_attribute('title').strip()
                d['brand'] = brand_func(item)
                d['category'] = 'mobile phones'#cat_name.lower()
                d['source'] = 'amazon.in'
                mongo_write(coll, d)

            try:
                next_page = driver.find_element_by_xpath('.//a[@id="pagnNextLink"]/span[@id="pagnNextString"]')
                next_page.click()
            except:
                driver.quit()
                break

            time.sleep(5)
          

if __name__ == "__main__":
    client, coll = mongo_open('short_collection')
    coll.delete_many({'source': 'amazon.in'})
    url = 'http://www.amazon.in/gp/site-directory/ref=nav_shopall_btn'
    urls = scraping_cats(url)
    scraping_cat(urls, coll)
    client.close()

