import time, re
from com_functions import selenium_spider


cat_list = [
'Audio & Home Entertainment',
#'Automotive',
#'Baby & Mom',
#'Books & Magazines',
'Cameras & Optics',
#'Charity',
#'Clothing & Accessories',
#'Coins & Notes',
#'Collectibles',
#'eBay Daily',
#'Fitness & Sports',
#'Fragrances, Beauty & Health',
#'Games, Consoles & Accessories',
'Home & Kitchen Appliances',
#'Home & Living',
#'Jewellery & Precious Coins',
#'Kitchen & Dining',
'Laptops & Computer Peripherals',
'LCD, LED & Televisions',
'Memory Cards, Pen Drives & HDD',
'Mobile Accessories',
'Mobile Phones',
#'Motor Classifieds',
#'Movies & Music',
#'Musical Instruments',
#'Shoes',
#'Stamps',
#'Stationery & Office Supplies',
'Tablets & Accessories',
#'Tools , Hardware & Electricals',
#'Toys, Games & School Supplies',
#'Warranty Services',
#'Watches',
'Wearable Devices',
#'Everything Else'
]

def scraping_categories(url, fh):
    driver = selenium_spider(url)
    time.sleep(5)
    parsed_cats = []
    while True:
        d = {}
        button = driver.find_element_by_xpath('.//td[@class="gh-td"]/input[@type="submit"]')
        cats = driver.find_elements_by_xpath('.//div[@id="gh-cat-box"]/select/option')
        cats = [x for x in cats if x.text not in parsed_cats and x.text in cat_list]
        if len(cats) == 0: break
        cat = cats[0]
        d['cat_name'] = cat.text
        parsed_cats.append(d['cat_name'])
        cat.click()
        time.sleep(1)
        button.click()
        #####
        time.sleep(5)
        second_url, total_items = scraping_pages(driver, driver.current_url)
        d['first_url'] = driver.current_url
        d['second_url'] = second_url
        d['total_items'] = total_items
        d['pages'] = page_count(total_items)
        line = '%s,\n' % d
        fh.write(line)
        #####

    driver.quit()

def scraping_pages(driver, f_url):
    count = 0
    while True:
        if count == 1: break
        #page_items = driver.find_elements_by_xpath('.//ul[@id="ListViewInner"]/li')
        total_items = driver.find_element_by_xpath('.//span[@class="listingscnt"]').text
        total_items = int(re.findall(r'([0-9,.]+)', total_items)[0].replace(',', ''))
        next_page = driver.find_element_by_xpath('.//td[@class="pagn-next"]')
        #current_page = driver.find_element_by_xpath('.//td[@class="pages"]/a[@class="pg curr"]').text
        next_page.click()
        time.sleep(5)
        url = driver.current_url
        count += 1

    return url, total_items

def page_count(total_items):
    total = total_items / 50 + 50
    return total

def main():
    url = 'http://www.ebay.in'
    fh = open('urls.py', 'w')
    fh.write('urls = [\n')
    scraping_categories(url, fh)
    fh.write(']')
    fh.close()
    
main()

