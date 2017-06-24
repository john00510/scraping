#coding: utf8
import time, re, sys
from com_functions import csv_writer, mongo_writer
from datetime import datetime


def amazon_item_parser(response, fh, coll):
    def name_func(response):
        name = response.xpath('.//h1[@id="title"]/span/text()').extract()[0].strip()
        return name

    def price_func(response):
        try:
            prices = response.xpath('.//div[@id="price"]/table/tr/td/span/text()').extract()
            prices = [p.strip() for p in prices if len(p.strip())!=0]
            price = prices[0]
            offer_price = prices[1]
            discount = response.xpath('.//tr[@id="regularprice_savings"]/td/text()').extract()[1]
            discount = re.findall(r'([0-9*]%)', discount)[0]
        except:
            try:
                price = response.xpath('.//span[@id="priceblock_ourprice"]/text()').extract()[0].strip()
                offer_price = None
                discount = None
            except:
                price = None
                offer_price = None
                discount = None
        return price, offer_price, discount

    def brand_func(response):
        brand = response.xpath('.//a[@id="brand"]/text()').extract()[0].strip()
        return brand

    def features_func(response):
        l = {}
        s = ''
        rows = response.xpath('.//div[@class="section techD"]/div[contains(@class, "content")]/div/div/table/tbody/tr')
        for row in rows:
            row = row.xpath('.//td/text()').extract()
            if len(row) != 2:
                continue
            label = row[0].strip()
            value = row[1].strip()
            if len(label) == 0 or len(value) == 0:
                continue
            l[label] = value
            line = '%s: %s, ' % (label, value)
            s += line
        s = s.strip().strip(',') + '.'
        return s, l

    def shipping(response):
        shipping = response.xpath('.//span[@id="price-shipping-message"]/b/text()').extract()
        if 'FREE Delivery' in shipping:
            return 1
        else:
            return 0

    def in_stock(response):
        instock = response.xpath('.//div[@id="availability"]/span/text()').extract()[0].strip().lower()
        if 'in stock' in instock:
            return 1
        else:
            return 0

    def color_func(feats_dict):
        try:
            return feats_dict['Colour']
        except:
            return None

    def descr(response):
        feats = response.xpath('.//div[@id="feature-bullets"]/ul/li/span/text()').extract()
        feats = [f.strip() for f in feats]
        descr = '; '.join(feats)+'.'
        return descr

    def group_func(response):
        group = response.xpath('.//div[@id="showing-breadcrumbs_div"]/div/div/ul/li/span[@class="a-list-item"]/a/text()').extract()[-1].strip()
        return group

    def imageurl_func(response):
        image = response.xpath('.//img[@id="landingImage"]/@src').extract()[0]
        return image

    def ref_id(feats_dict):
        try:
            return feats_dict['ASIN']
        except:
            return None

    pr, of_pr, disc = price_func(response)
    feats_line, feats_dict = features_func(response)

    d = {}
    d['name'] = name_func(response)
    d['permalink'] = None 
    d['create_date'] = datetime.now().strftime('%d-%m-%Y %H:%M')
    d['mrp'] = None
    d['price'] = pr
    d['offer_price'] = of_pr
    d['discount'] = disc
    d['store_id'] = None
    d['category'] = group_func(response)
    d['category_id'] = None
    d['source'] = 'amazon.in'
    d['data_source'] = 'amazon.in'
    d['ref_id'] = ref_id(feats_dict)
    d['url'] = response.url
    d['image_url'] = imageurl_func(response)
    d['deal_notes'] = None
    d['meta_title'] = d['name']
    d['meta_key'] = None
    d['meta_des'] = None
    d['size'] = None
    d['size_unit'] = None
    d['features'] = feats_line
    d['description'] = descr(response)
    d['key_features'] = None
    d['color'] = color_func(feats_dict)
    d['brand'] = brand_func(response)
    d['specifications'] = feats_line
    d['offers'] = None
    d['in_stock'] = in_stock(response)
    d['free_shipping'] = shipping(response)
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

