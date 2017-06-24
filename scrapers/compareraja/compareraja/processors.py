from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os


def chrome_spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.set_window_size(600, 800)
    driver.get(url)
    time.sleep(5)
    return driver

def scrape_item(response):
    def get_features(repsonse):
        feats = response.xpath('.//ul[@class="fedet"]')
        l = []
        for f in feats:
            d = {}
            d2 = {}
            group = f.xpath('./li[@class="tp"]/text()').extract()[0].strip()
            for e in f.xpath('./li'):
                try:
                    e1 = e.xpath('./p/text()').extract()[0].strip().replace('.', ',')
                    e2 = e.xpath('./span/text()').extract()[0].strip()
                    d2[e1] = e2                              
                except:
                    pass
            d[group] = d2
            l.append(d)
        return l

    def get_stores(response):
        elements = response.xpath('.//div[@class="Prices Pricesnew"]/ul[contains(@class, "nemcomp-price-row-nw")][contains(@id, "ComparePrice1")]')
        dd = {}
        for e in elements:
            d = {}
            merchant = e.xpath('.//p[@class="merlogoli"]/span/@class').extract()[0]
            d['price'] = e.xpath('./li[@class="cp-c5"]/span/span/text()').extract()[0].replace('Rs.', '').strip()
            d['url'] = e.xpath('./li[@class="cp-c6"]/a/@href').extract()[0]
            dd[merchant] = d
        return dd

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

    coll = response.meta['coll']
    fh = response.meta['fh']
    d = {}
    d['name'] = response.meta['name']
    d['category'] = response.meta['category']
    d['source'] = response.meta['source']
    d['url'] = response.meta['url']
    d['image_url'] = get_image(response)
    d['features'] = get_features(response)
    d['merchants'] = get_stores(response)
    coll.insert(d)
    write_csv(fh, d['name'], d['category'], d['url'], d['source'], d['features'], d['merchants'], d['image_url']) 

def open_csv(fn):
    fn = '/'.join(os.path.abspath('').split('/')[:-3])+'/output/compareraja/' + fn + '.csv'
    header = 'name,category,url,image_url,source,amazon_link,amazon_price,ebay_link,ebay_price,flipkart_link,flipkart_price,tatacliq_link,tatacliq_price,shopclues_link,shopclues_price,snapdeal_link,snapdeal_price,gadgets_link,gadgets_price,features\n'
    fh = open(fn, 'wb')
    fh.write(header)
    return fh

def write_csv(fh, name, cat, url, src, features, d, image_url):
    name = name.replace('"', ' ')
    feats = str(features).replace('"', "'")
    try:
        am_url = d['amazon']['url']
        am_prc = d['amazon']['price']
    except:
        am_url = None
        am_prc = None
    try:
        eb_url = d['ebay']['url']
        eb_prc = d['ebay']['price']
    except:
        eb_url = None
        eb_prc = None
    try:
        fl_url = d['flipkart']['url']
        fl_prc = d['flipkart']['price']
    except:
        fl_url = None
        fl_prc = None
    try:
        ta_url = d['tatacliq']['url']
        ta_prc = d['tatacliq']['price']
    except:
        ta_url = None
        ta_prc = None
    try:
        sh_url = d['shopclues']['url']
        sh_prc = d['shopclues']['price']
    except:
        sh_url = None
        sh_prc = None
    try:
        sn_url = d['snapdeal']['url']
        sn_prc = d['snapdeal']['price']
    except:
        sn_url = None
        sn_prc = None
    try:
        ga_url = d['gadgets']['url']
        ga_prc = d['gadgets']['price']
    except:
        ga_url = None
        ga_prc = None
    line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name, cat, url, image_url, src, am_url, am_prc, eb_url, eb_prc, fl_url, fl_prc, ta_url, ta_prc, sh_url, sh_prc, sn_url, sn_prc, ga_url, ga_prc, feats)
    fh.write(line.encode('utf-8')) 

