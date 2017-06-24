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
            return re.findall(r'([0-9%-]+)', discount)[0]
        except:
            return None


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
            return features['Color Family']
        except:
            return None

    def in_stock(response):
        instock = response.meta['in_stock']
        if 'OUT OF STOCK' in instock:
            return 0
        else:
            return 1

    def offer_func(response):
        try:
            return response.xpath('.//div[contains(@class, "pdp-title")]/text()').extract()[1].strip()
        except:
            return None

    def brand_func(response):
        try:
            return response.xpath('.//h3[@itemprop="brand"]/span/text()').extract()[0]
        except:
            return None

    def image_func(response):
        images = response.xpath('.//img/@src').extract()
        image = [i for i in images if 'img.tatacliq.com' in i][0]
        return image

    d = {}
    d['name'] = response.xpath('.//h1[@class="product-name"]/text()').extract()[0]
    d['permalink'] = None 
    d['create_date'] = None
    d['mrp'] = None
    d['price'] = response.meta['price']
    d['offer_price'] = response.meta['offer_price']
    d['discount'] = response.meta['discount']
    d['store_id'] = None
    d['category'] = response.xpath('.//ul[@class="breadcrumbs wrapper"]/li/a/text()').extract()[2].lower().strip()
    d['category_id'] = None
    d['source'] = 'tatacliq.com'
    d['data_source'] = 'tatacliq.com'
    d['ref_id'] = None
    d['url'] = response.url
    d['image_url'] = image_func(response)
    d['description'] = descr(response)
    d['deal_notes'] = None
    d['meta_title'] = None
    d['meta_key'] = None
    d['meta_des'] = None
    d['brand'] = brand_func(response)
    d['size'] = None
    d['size_unit'] = None
    d['key_features'] = None
    d['features'] = specs(response)
    d['color'] = colors(d['features'])
    d['specifications'] = None
    d['offers'] = offer_func(response)
    d['in_stock'] = in_stock(response)
    d['free_shipping'] = 0
    d['shippingCharge'] = None
    d['mm_average_rating'] = None
    d['is_deal'] = None
    d['is_coupon'] = None
    d['start_date'] = None
    d['end_date'] = None
    d['coupon_code'] = None
    d['special_deal'] = None
    d['upcoming_deal'] = None
    d['show_as_banner'] = None
    d['local_store_deal'] = None
    d['localstore_deal_enabled'] = None
    d['featured'] = None
    d['enabled'] = None
    d['no_cashback'] = None
    d['base_product'] = None
    d['match_set'] = None
    d['match_attempt'] = None
    d['store_count'] = None
    d['display_order'] = None
    d['last_update'] = None
    d['deleted'] = None
    mongo_writer(coll, d)
    csv_writer(fh, d['name'],d['permalink'],d['create_date'],d['mrp'],d['price'],d['offer_price'],d['discount'],\
               d['store_id'],d['category'],d['category_id'],d['source'],d['data_source'],d['ref_id'],d['url'],d['image_url'],\
               d['description'],d['deal_notes'],\
               d['meta_title'],d['meta_key'],d['meta_des'],d['brand'],d['size'],d['size_unit'],d['color'],d['key_features'],\
               d['features'],d['specifications'],d['offers'],d['in_stock'],d['free_shipping'],d['shippingCharge'],\
               d['mm_average_rating'],d['is_deal'],d['is_coupon'],d['start_date'],d['end_date'],d['coupon_code'],\
               d['special_deal'],d['upcoming_deal'],d['show_as_banner'],d['local_store_deal'],d['localstore_deal_enabled'],\
               d['featured'],d['enabled'],d['no_cashback'],d['base_product'],d['match_set'],d['match_attempt'],d['store_count'],\
               d['display_order'],d['last_update'],d['deleted'])


