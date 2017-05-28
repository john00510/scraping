import re, sys, os
sys.path.append('/'.join(os.path.abspath('').split('/')[:-3])+'/functions')
from com_functions import csv_writer, log_writer

def tatacliq_items_parser(item):
    def price(item):
        try:
            item_price = item.xpath('.//p[@class="old"]/span/span/text()').extract()[0]
        except:
            item_price = item.xpath('.//div[@class="price"]/span[@class="priceFormat"]/span/text()').extract()[0]
        item_price = re.findall(r'([0-9.]+)', item_price)[0]
        return item_price

    def offer_price(item, price):
        try:
            offer_price = item.xpath('.//p[@class="sale"]/span/span/text()').extract()[0]
            offer_price = re.findall(r'([0-9.]+)', offer_price)[0]
        except:
            offer_price = price
        return offer_price

    def discount(item):
        try:
            discount = item.xpath('.//p[@class="savings"]/span/text()').extract()[0]
            discount = re.findall(r'([0-9%-]+)', discount)[0]
        except:
            discount = ''
        return discount

    price = price(item)
    offer_price = offer_price(item, price)
    discount = discount(item)
    return price, offer_price, discount

def tatacliq_item_parser(response, fh):
    def descr(response):
        descr1 = response.xpath('.//li[@itemprop="description"]/text()').extract()[0].strip() 
        descr2 = response.xpath('.//ul[@class="item-desc"]/following-sibling::ul/li/text()').extract() 
        descr2 = '. '.join(descr2)  
        descr = descr1 + ' ' + descr2  
        return descr

    def specs(response):
        l = {}
        specs = response.xpath('.//ul[@class="tabs pdp specTabs"]/li')
        for spec in specs:
            sp = spec.xpath('./div/ul/li')
            for s in sp:
                l[s.xpath('./span/text()').extract()[0].strip()] = s.xpath('./span/text()').extract()[1].strip()       
        return l

    def colors(features):
        try:
            color = features['Color Family']
        except:
            color = ''
        return color

    def in_stock(response):
        instock = response.xpath('.//div[@id="allVariantOutOfStock"]/@style').extract()[0]
        return instock

    def offer_func(response):
        try:
            offer = response.xpath('.//div[contains(@class, "pdp-title")]/text()').extract()[1].strip()
        except:
            offer = ''
        return offer

    id = ''
    name = response.xpath('.//h1[@class="product-name"]/text()').extract()[0]
    permalink = '' 
    create_date = ''
    mrp = ''
    price = response.meta['price']
    offer_price = response.meta['offer_price']
    discount = response.meta['discount']
    store_id = ''
    category_id = response.xpath('.//ul[@class="breadcrumbs wrapper"]/li/a/text()').extract()[2]
    data_source = 'tatacliq.com'
    ref_id = ''
    url = response.url
    description = descr(response)
    deal_notes = ''
    meta_title = ''
    meta_key = ''
    meta_des = name
    brand = response.xpath('.//h3[@itemprop="brand"]/span/text()').extract()[0]
    size = ''
    size_unit = ''
    key_features = ''
    features = specs(response)
    color = colors(features)
    specifications = ''
    offers = offer_func(response)
    in_stock = in_stock(response)
    free_shipping = 0
    shippingCharge = ''
    mm_average_rating = ''
    is_deal = ''
    is_coupon = ''
    start_date = ''
    end_date = ''
    coupon_code = ''
    special_deal = ''
    upcoming_deal = ''
    show_as_banner = ''
    local_store_deal = ''
    localstore_deal_enabled = ''
    featured = ''
    enabled = ''
    no_cashback = ''
    base_product = ''
    match_set = ''
    match_attempt = ''
    store_count = ''
    display_order = ''
    last_update = ''
    deleted = ''
    csv_writer(fh, id,name,permalink,create_date,mrp,price,offer_price,discount,store_id,category_id,\
               data_source,ref_id,url,description,deal_notes,meta_title,meta_key,meta_des,brand,\
               size,size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
               shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
               special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
               featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
               display_order,last_update,deleted)
