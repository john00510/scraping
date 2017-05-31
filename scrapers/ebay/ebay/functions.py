import time, re
from com_functions import csv_writer, mongo_writer
from datetime import datetime


def ebay_item_parser(response, fh, category, coll):
    def name_func(response):
        name = response.xpath('.//h1[@id="itemTitle"]/text()').extract()[0]
        return name

    def price_func(response):
        try:
            price = response.xpath('.//span[@itemprop="price"]/text()').extract()[0].split(' ')[1]
            offer_price = price
            discount = ''
        except:
            price = response.xpath('.//span[@id="mm-saleOrgPrc"]/text()').extract()[0].split(' ')[1]
            offer_price = response.xpath('.//span[contains(text(), "Discounted price")]/\
                following-sibling::span/text()').extract()[0].split(' ')[1]
            discount = response.xpath('.//div[@id="mm-saleAmtSavedPrc"]/text()').extract()[0].strip()
            discount = re.findall(r'([0-9]+%)', discount)[0]
        return price, offer_price, discount

    def brand_func(response):
        brand = response.xpath('.//td[@class="attrLabels"][contains(text(), "Brand:")]/following-sibling\
                ::td/span/text()').extract()[0]
        return brand

    def features_func(response):
        d = {}
        features = response.xpath('.//h2[contains(text(), "Item specifics")]/following-sibling::table/tr')
        d['Condition'] = features[0].xpath('./td/div/text()').extract()[0].strip().strip(':')
        try:
            d['Brand'] = features[0].xpath('./td/span/text()').extract()[0].strip()
        except:
            d['Brand'] = ''
        for feature in features[1:]:
            try:
                d[feature.xpath('./td/text()').extract()[0].strip().strip(':')] = feature.xpath('./td/span/text()')\
                    .extract()[0]
                d[feature.xpath('./td/text()').extract()[2].strip().strip(':')] = feature.xpath('./td/span/text()')\
                    .extract()[1]
            except:
                d[feature.xpath('./td/text()').extract()[0].strip().strip(':')] = feature.xpath('./td/span/text()')\
                    .extract()[0]
        return d

    def ref_number(response):
        ref_number = response.xpath('.//div[@id="descItemNumber"]/text()').extract()[0].strip()
        return ref_number

    def shipping(response):
        shipping = response.xpath('.//span[@id="shSummary"]/span/span/text()').extract()
        if 'FREE' in shipping:
            shipping = 1
        else:
            shipping = 0
        return shipping

    def color_func(features):
        try:
            color = features['Colour']
        except:
            color = ''
        return color

    def descr(features):
        s = ''
        for x, y in features.items():
            s += x + ': ' + y + ', '
        s = s.strip().strip(',') + '.'
        return s

    pr, of_pr, disc = price_func(response)

    d = {}
    d['id'] = ''
    d['name'] = name_func(response)
    d['permalink'] = '' 
    d['create_date'] = ''
    d['mrp'] = ''
    d['price'] = pr
    d['offer_price'] = of_pr
    d['discount'] = disc
    d['store_id'] = ''
    d['category_id'] = category 
    d['data_source'] = 'ebay.in'
    d['ref_id'] = ref_number(response)
    d['url'] = response.url
    d['deal_notes'] = ''
    d['meta_title'] = d['name']
    d['meta_key'] = ''
    d['meta_des'] = d['name']
    d['size'] = ''
    d['size_unit'] = ''
    d['features'] = features_func(response)
    d['description'] = descr(d['features'])
    d['key_features'] = ''
    d['color'] = color_func(d['features'])
    d['brand'] = d['features']['Brand']
    d['specifications'] = ''
    d['offers'] = ''
    d['in_stock'] = ''
    d['free_shipping'] = shipping(response)
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

