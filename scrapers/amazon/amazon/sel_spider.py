#encoding: utf8
from com_functions import selenium_spider, mongo_db
from groups import groups
import time, re


def total_count(driver):
    tc = driver.find_element_by_xpath('.//h2[@id="s-result-count"]').text
    print tc
    try:
        tc = re.findall(r' ([0-9,.]+) ', tc)[0].replace(',', '')
    except:
        tc = re.findall(r'^([0-9]+) ', tc)[0]
    return tc

def mobile_exc(driver):
    try:
        driver.find_elements_by_xpath('.//span[@class="a-list-item"]/a/span[contains(text(), "Basic Mobiles")]').click()
        time.sleep(5)
        return driver
    except:
        print 'mobile exception error'

def brand_func(driver):
    try:
        return item.find_element_by_xpath('.//span[contains(text(), "by")]/following-sibling::span').text.lower()
    except:
        return None

def scraping_cats(url):
    driver = selenium_spider(url)
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

def scraping_cat(urls, fh):
    for u in urls:
        url = u['url']
        cat_name = u['cat_name'].lower()
        driver = selenium_spider(url)
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
                url = item.find_element_by_xpath('.//a[@title]').get_attribute('href')
                #name = item.find_element_by_xpath('.//a[@title]').get_attribute('title')
                #brand = brand_func(driver)
                line = '%s\n' % url
                fh.write(line)

            try:
                next_page = driver.find_element_by_xpath('.//a[@id="pagnNextLink"]/span[@id="pagnNextString"]')
                next_page.click()
            except:
                driver.quit()
                break

            time.sleep(5)
          

if __name__ == "__main__":
    fh = open('scr_urls.txt', 'w')
    url = 'http://www.amazon.in/gp/site-directory/ref=nav_shopall_btn'
    urls = scraping_cats(url)
    scraping_cat(urls, fh)
    fh.close()

