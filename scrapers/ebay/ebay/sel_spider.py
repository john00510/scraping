import time
from com_functions import selenium_spider


cat_list = [
#'Audio & Home Entertainment',
#'Automotive',
#'Baby & Mom',
#'Books & Magazines',
#'Cameras & Optics',
#'Charity',
#'Clothing & Accessories',
#'Coins & Notes',
#'Collectibles',
#'eBay Daily',
#'Fitness & Sports',
#'Fragrances, Beauty & Health',
#'Games, Consoles & Accessories',
#'Home & Kitchen Appliances',
#'Home & Living',
#'Jewellery & Precious Coins',
#'Kitchen & Dining',
#'Laptops & Computer Peripherals',
#'LCD, LED & Televisions',
#'Memory Cards, Pen Drives & HDD',
#'Mobile Accessories',
'Mobile Phones',
#'Motor Classifieds',
#'Movies & Music',
#'Musical Instruments',
#'Shoes',
#'Stamps',
#'Stationery & Office Supplies',
#'Tablets & Accessories',
#'Tools , Hardware & Electricals',
#'Toys, Games & School Supplies',
#'Warranty Services',
#'Watches',
#'Wearable Devices',
#'Everything Else'
]

def scraping_categories(url):
    
    driver = selenium_spider(url)
    time.sleep(3)
    parsed_cats = []
    li = []
    while True:
        button = driver.find_element_by_xpath('.//td[@class="gh-td"]/input[@type="submit"]')
        cats = driver.find_elements_by_xpath('.//div[@id="gh-cat-box"]/select/option')
        cats = [x for x in cats if x.text not in parsed_cats and x.text in cat_list]
        if len(cats) == 0: break
        cat = cats[0]
        cat_name = cat.text
        parsed_cats.append(cat_name)
        cat.click()
        time.sleep(1)
        button.click()
        #####
        time.sleep(5)
        first_url = driver.current_url
        l = scraping_pages(driver, first_url)
        l.append(cat_name)
        li.append(l)
        #####

    driver.quit()
    return li

def scraping_pages(driver, f_url):
    count = 0
    l = []
    while True:
        if count == 1: break
        l.append(f_url)
        #items = driver.find_elements_by_xpath('.//ul[@id="ListViewInner"]/li')
        next_page = driver.find_element_by_xpath('.//td[@class="pagn-next"]')
        #current_page = driver.find_element_by_xpath('.//td[@class="pages"]/a[@class="pg curr"]').text
        #print len(items)
        next_page.click()
        time.sleep(5)
        l.append(driver.current_url)
        count += 1

    return l

def main():
    url = 'http://www.ebay.in'
    l = scraping_categories(url)
    return l

