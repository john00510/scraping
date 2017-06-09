from com_functions import selenium_spider
from selenium.webdriver.common.action_chains import ActionChains
import time, re
from sel_urls import urls


def hover(driver, element):
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()

def error_func(driver):
    try:
        driver.find_element_by_xpath('.//div[@class="toptext letterSpace"]/span[contains(text(), "Internal Server Error")]')
    except:
        pass

def scroll_to_element(driver): 
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('.//div[@id="see-more-products"][contains(@style, "visible")]'))

def check_ip(url):
    driver = selenium_spider(url)
    time.sleep(10)
    driver.quit()

def scraping_cats(fh):
    for url in urls:
        scraping_cat(url, fh)

def items_found(driver):
    items = driver.find_elements_by_xpath('.//span[@class="totalCountHead"]/i')[1].get_attribute('innerHTML')
    return items

def scraping_cat(url, fh):
    driver = selenium_spider(url)
    #error_func(driver)
    total = items_found(driver)
    scraping_items(driver, fh, total)
    driver.quit() 

def scraping_items(driver, fh, total):
    l = []
    scrd = 0
    c = 0
    category = driver.find_element_by_xpath('.//h1[@class="category-name"]').get_attribute('category').lower()
    while True:
        urls = driver.find_elements_by_xpath('.//section[@data-dpwlbl="Product Grid"]/div[contains(@class, "product-tuple-listing")]/div[contains(@class, "product-tuple-description")]/div[contains(@class, "product-desc-rating")]/a[@href]')
        urls = [x.get_attribute('href') for x in urls]
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

    for url in l:
        line = '%s\n' % url
        fh.write(line)

def main():
    fh = open('scr_urls.txt', 'w')
    scraping_cats(fh)
    fh.close()

main()

