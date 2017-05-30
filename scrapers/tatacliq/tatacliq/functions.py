import re
from com_functions import csv_writer, mongo_writer
from datetime import datetime

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

def tatacliq_item_parser(response, fh, coll):
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

    d = {}
    d['id'] = ''
    d['name'] = response.xpath('.//h1[@class="product-name"]/text()').extract()[0]
    d['permalink'] = '' 
    d['create_date'] = ''
    d['mrp'] = ''
    d['price'] = response.meta['price']
    d['offer_price'] = response.meta['offer_price']
    d['discount'] = response.meta['discount']
    d['store_id'] = ''
    d['category_id'] = response.xpath('.//ul[@class="breadcrumbs wrapper"]/li/a/text()').extract()[2]
    d['data_source'] = 'tatacliq.com'
    d['ref_id'] = ''
    d['url'] = response.url
    d['description'] = descr(response)
    d['deal_notes'] = ''
    d['meta_title'] = ''
    d['meta_key'] = ''
    d['meta_des'] = d['name']
    d['brand'] = response.xpath('.//h3[@itemprop="brand"]/span/text()').extract()[0]
    d['size'] = ''
    d['size_unit'] = ''
    d['key_features'] = ''
    d['features'] = specs(response)
    d['color'] = colors(d['features'])
    d['specifications'] = ''
    d['offers'] = offer_func(response)
    d['in_stock'] = in_stock(response)
    d['free_shipping'] = 0
    d['shippingCharge'] = ''
    d['mm_average_rating'] = ''
    d['is_deal'] = ''
    d['is_coupon'] = ''
    d['start_date'] = ''
    d['end_date'] = ''
    d['coupon_code'] = ''
    d['special_deal'] = ''
    d['upcoming_deal'] = ''
    d['show_as_banner'] = ''
    d['local_store_deal'] = ''
    d['localstore_deal_enabled'] = ''
    d['featured'] = ''
    d['enabled'] = ''
    d['no_cashback'] = ''
    d['base_product'] = ''
    d['match_set'] = ''
    d['match_attempt'] = ''
    d['store_count'] = ''
    d['display_order'] = ''
    d['last_update'] = ''
    d['deleted'] = ''
    d['_id'] = {'item_url': d['url'], 'date': str(datetime.now().date())}
    mongo_writer(coll, d)
    csv_writer(fh, d['id'],d['name'],d['permalink'],d['create_date'],d['mrp'],d['price'],d['offer_price'],d['discount'],\
               d['store_id'],d['category_id'],d['data_source'],d['ref_id'],d['url'],d['description'],d['deal_notes'],\
               d['meta_title'],d['meta_key'],d['meta_des'],d['brand'],d['size'],d['size_unit'],d['color'],d['key_features'],\
               d['features'],d['specifications'],d['offers'],d['in_stock'],d['free_shipping'],d['shippingCharge'],\
               d['mm_average_rating'],d['is_deal'],d['is_coupon'],d['start_date'],d['end_date'],d['coupon_code'],\
               d['special_deal'],d['upcoming_deal'],d['show_as_banner'],d['local_store_deal'],d['localstore_deal_enabled'],\
               d['featured'],d['enabled'],d['no_cashback'],d['base_product'],d['match_set'],d['match_attempt'],d['store_count'],\
               d['display_order'],d['last_update'],d['deleted'])

