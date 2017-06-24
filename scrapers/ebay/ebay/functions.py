import time, re
from com_functions import mongo_write
from datetime import datetime


def ebay_item_parser(response):
    coll = response.meta['coll']
    category = response.meta['category']
    name = response.meta['name']
    source = response.meta['source']
    url = response.meta['url']


    def price_func(response):
        try:
            price = response.xpath('.//span[@itemprop="price"]/text()').extract()[0].split(' ')[1].strip()
            offer_price = price
            discount = None
        except:
            price = response.xpath('.//span[@id="mm-saleOrgPrc"]/text()').extract()[0].split(' ')[1].strip()
            offer_price = response.xpath('.//span[contains(text(), "Discounted price")]/\
                following-sibling::span/text()').extract()[0].split(' ')[1].strip()
            discount = response.xpath('.//div[@id="mm-saleAmtSavedPrc"]/text()').extract()[0].strip()
            discount = re.findall(r'([0-9]+%)', discount)[0]
        return price, offer_price, discount

    def brand_func(response):
        try:
            brand = response.xpath('.//td[@class="attrLabels"][contains(text(), "Brand:")]/following-sibling\
                    ::td/span/text()').extract()[0].strip().lower()
        except:
            try:
                brand = d['features']['Brand'].strip().lower()
            except:
                brand = 'uknown'
        if brand == '-':
            brand = 'uknown'
        if brand == '':
            brand = 'uknown'
        return brand.lower()

    def features_func(response):
        d = {}
        features = response.xpath('.//h2[contains(text(), "Item specifics")]/following-sibling::table/tr')
        try:
            d['Condition'] = features[0].xpath('./td/div/text()').extract()[0].strip().strip(':')
        except:
            d['Condition'] = ''
        try:
            d['Brand'] = features[0].xpath('./td/span/text()').extract()[0].strip()
        except:
            d['Brand'] = ''
        for feature in features[1:]:
            try:
                d[feature.xpath('./td/text()').extract()[0].strip().strip(':').replace('.', '')] = feature.xpath('./td/span/text()')\
                    .extract()[0]
                d[feature.xpath('./td/text()').extract()[2].strip().strip(':').replace('.', '')] = feature.xpath('./td/span/text()')\
                    .extract()[1]
            except:
                d[feature.xpath('./td/text()').extract()[0].strip().strip(':').replace('.', '')] = feature.xpath('./td/span/text()')\
                    .extract()[0]
        return d

    def ref_number(response):
        ref_number = response.xpath('.//div[@id="descItemNumber"]/text()').extract()[0].strip()
        return ref_number

    def shipping(response):
        shipping = response.xpath('.//span[@id="shSummary"]/span/span/text()').extract()
        if 'FREE' in shipping:
            return 1
        else:
            return 0

    def color_func(features):
        try:
            return features['Colour']
        except:
            return None

    def descr(features):
        s = ''
        for x, y in features.items():
            s += x + ': ' + y + ', '
        s = s.strip().strip(',') + '.'
        return s

    def image_func(response):
        image = response.xpath('.//img[@itemprop="image"]/@src').extract()[0]
        return image

    pr, of_pr, disc = price_func(response)

    d = {}
    d['name'] = name
    d['permalink'] = None 
    d['create_date'] = datetime.now().strftime('%d-%m-%Y %H:%M')
    d['mrp'] = None
    d['price'] = pr
    d['offer_price'] = of_pr
    d['discount'] = disc
    d['store_id'] = None
    d['category'] = category
    d['category_id'] = None 
    d['source'] = source
    d['data_source'] = source
    d['ref_id'] = ref_number(response)
    d['url'] = url
    d['image_url'] = image_func(response)
    d['deal_notes'] = None
    d['meta_title'] = d['name']
    d['meta_key'] = None
    d['meta_des'] = None
    d['size'] = None
    d['size_unit'] = None
    d['features'] = features_func(response)
    d['description'] = descr(d['features'])
    d['key_features'] = None
    d['color'] = color_func(d['features'])
    d['brand'] = brand_func(response)
    d['specifications'] = None
    d['offers'] = None
    d['in_stock'] = None
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
    mongo_write(coll, d)

