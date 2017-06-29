from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os, re, uuid, datetime


def chrome_spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)
    return driver

def scrape_item(response):
    def get_features(repsonse):
        feats = response.xpath('.//ul[@class="fedet"]')
        l = ''
        for f in feats:
            group = f.xpath('./li[@class="tp"]/text()').extract()[0].strip()
            for e in f.xpath('./li'):
                try:
                    e1 = e.xpath('./p/text()').extract()[0].strip().replace('.', ',')
                    e2 = e.xpath('./span/text()').extract()[0].strip() 
                    if 'no' in e2.lower():
                        continue      
                    if 'yes' in e2.lower():
                        l2 = e1
                    else:
                        l2 = '%s %s' % (e1, e2)
                    l += l2 + ' | '                      
                except:
                    pass
        return l.strip().strip('|').strip()

    def get_price(e):
        if len(e.xpath('./div/p[@class="mertext"]/span/text()').extract()) == 0:
            return e.xpath('./div/p[@class="mertext"]/text()').extract()[0].strip().split(' ')[1]
        else:
            return e.xpath('./div/p[@class="mertext"]/span/text()').extract()[1].strip()

    def get_image(response):
        try:
            image = response.xpath('.//a[@class="simpleLens-lens-image"]/@data-lens-image').extract()[0]
        except:
            image = response.xpath('.//a[@class="simpleLens-lens-image"]/img/@src').extract()[0]
        return image

    def get_url(e):
        url = e.xpath('./li[@class="cp-c6"]/a/@onclick').extract()[0]
        url = re.findall(r"'(http.+?)',", url)[0]
        if 'amazon' in url:
            return url
        if 'ebay' in url:
            return url
        if 'flipkart' in url:
            return url
        if 'shopclues' in url:
            return url
        if 'snapdeal' in url:
            return
        if 'tatacliq' in url:
            return url
        if 'gadgetsnow' in url:
            return url
        else:
            return None

    def get_source(store):
        return store

    def get_category_id(category):
        if category == 'mobile phones':
            return 7
        if category == 'tablets':
            return 7
        if category == 'televisions':
            return 9
        if category == 'air_conditioners': # air conditioners air coolers
            return 23
        if category == 'laptops':
            return 8
        if category == 'washing_machines':
            return 20
        if category == 'refrigerators':
            return 21
        if category == 'cameras':
            return 11
        if category == 'water purifiers':
            return 22
        if category == 'microwave_ovens':
            return 22
        if category == 'printers':
            return 12
        if category == 'trimmers': # personal care
            return 24

    def get_store_id(merchant):
        if merchant == 'amazon': #
            return 2
        if merchant == 'ebay':
            return 417
        if merchant == 'flipkart': 
            return 1
        if merchant == 'shopclues': #
            return 3
        if merchant == 'tatacliqli': #
            return 4
        if merchant == 'snapdeal': #
            return 5

    cur = response.meta['cur']
    conn = response.meta['conn']

    elements = response.xpath('.//div[@class="Prices Pricesnew"]/ul[contains(@class, "nemcomp-price-row-nw")][contains(@id, "ComparePrice1")]')
    match = {}
    for e in elements:
        _id = str(uuid.uuid4())
        merchant = e.xpath('.//p[@class="merlogoli"]/span/@class').extract()[0]
        store_id = get_store_id(merchant) #
        price = e.xpath('./li[@class="cp-c5"]/span/span/text()').extract()[0].replace('Rs.', '').strip()
        url = get_url(e) #
        print url
        name = response.meta['name'].replace('"', "'") #
        category_id = get_category_id(response.meta['category']) #
        data_source = get_source(merchant)
        comp_url = response.meta['url']
        image_url = get_image(response)
        features = get_features(response).replace('"', "'") #
        t = (_id, merchant)
        match[merchant] = _id
        #image_sql(cur, conn, _id, image_url)
        #product_sql(cur, conn, _id, name, category_id, url, comp_url, data_source, features, price)

    #match_sql(cur, conn, match)

def product_sql(cur, conn, _id, name, category_id, url, comp_url, data_source, features, price):
    create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO products (id, name, category_id, url, data_source, features, price, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (_id, name.encode('utf8'), category_id, url, data_source, features.encode('utf8'), price, create_date))
    conn.commit()

def image_sql(cur, conn, _id, image_url):
    cur.execute("INSERT INTO product_images (product_id, img1_url) VALUES (%s, %s)", (_id, image_url))
    conn.commit()

def match_sql(cur, conn, d):
    try:
        amazon = d['amazon']
    except:
        amazon = None
    try:
        ebay = d['ebay']
    except:
        ebay = None
    try:
        tatacliq = d['tatacliqli']
    except:
        tatacliq = None
    try:
        flipkart = d['flipkart']
    except:
        flipkart = None
    try:
        shopclues = d['shopclues']
    except:
        shopclues = None
    try:
        snapdeal = d['snapdeal']
    except:
        snapdeal = None
    cur.execute("INSERT INTO product_match (product_1, product_2, product_3, product_4, product_5, product_6) VALUES (%s, %s, %s, %s, %s, %s)", (flipkart, shopclues, amazon, snapdeal, ebay, tatacliq))
    conn.commit() 

def get_store(d, store):
    try:
        url = d[store]['url']
        price = d[store]['price']
    except:
        url = None
        price = None
    return price, url

'''
[
	"mobile phones",
	"tablets",
	"televisions",
	"air_conditioners",
	"laptops",
	"washing_machines",
	"refrigerators",
	"cameras",
	"water_purifiers",
	"microwave_ovens",
	"printers",
	"trimmers"
]
'''

