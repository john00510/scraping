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

def scrolling_down(driver):
    #scheight = 9.9
    while scheight > .1:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/.01);" #% scheight)
        scheight -= .01
        time.sleep(0.01)

def scroll_to_element(driver): 
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('.//div[@id="see-more-products"][contains(@style, "visible")]'))

def check_ip(url):
    driver = selenium_spider(url)
    time.sleep(10)
    driver.quit()

def scraping_cats(fh):
    for url in urls[:1]:
        scraping_cat(url, fh)

def items_found(driver):
    items = driver.find_element_by_xpath('.//div[@id="product_list"]/div[@class="product_found"]/span').text.split(' ')[0]
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
    category = driver.find_element_by_xpath('.//div[@class="page_heading"]/h1').text.lower()
    while True:
        rows = driver.find_elements_by_xpath('.//div[@id="product_list"]/div[@class="row"]')
        for row in rows:
            urls = row.find_elements_by_xpath('./div[contains(@class, "column")]/a[contains(@href, "http")]')
            urls = [url.get_attribute('href') for url in urls]

        if len(urls) == scrd:
            c += 1 
        l += urls
        l = list(set(l))
        print 'category: %s, total: %s, scraped: %s' % (category, total, len(urls))
        if int(total) == len(urls):
            break
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scrolling_down(driver)
        time.sleep(5)
        try:
            driver.find_element_by_xpath('.//div[@id="load_more"][contains(@style, "display")]').click()
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

