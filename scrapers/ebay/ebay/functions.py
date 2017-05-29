import time, re
from selenium import webdriver
from com_functions import csv_writer


def ebay_item_parser(response, fh, category):
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

    id = ''
    name = name_func(response)
    permalink = '' 
    create_date = ''
    mrp = ''
    price = pr
    offer_price = of_pr
    discount = disc
    store_id = ''
    category_id = category 
    data_source = 'ebay.in'
    ref_id = ref_number(response)
    url = response.url
    #print url, '####################################################'
    deal_notes = ''
    meta_title = name
    meta_key = ''
    meta_des = name
    size = ''
    size_unit = ''
    features = features_func(response)
    description = descr(features)
    key_features = ''
    color = color_func(features)
    brand = features['Brand']
    specifications = ''
    offers = ''
    in_stock = ''
    free_shipping = shipping(response)
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



