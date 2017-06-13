import time, re
from com_functions import csv_writer, mongo_writer 


def snapdeal_item_parser(response, fh, coll):
    def name_func(response):
        name = response.xpath('.//h1[@itemprop="name"]/text()').extract()[0].strip()
        return name

    def prices(response):
        try:
            price = response.xpath('.//div[contains(@class, "pdpCutPrice")]/text()').extract()[0].strip().strip('Rs.').strip()
            offer_price = response.xpath('.//span[@class="pdp-final-price"]/span/text()').extract()[0].strip()
            discount = response.xpath('.//span[contains(@class, "pdpDiscount")]/span/text()').extract()[0].strip() + '%'
        except:
            price = response.xpath('.//span[@itemprop="price"]/text()').extract()[0].strip().strip('Rs.').strip()
            offer_price = price
            discount = None
        return price, offer_price, discount

    def description_func(response):
        x = response.xpath('.//div[@class="tab-container"]/div/div[contains(@class, "spec-section expanded")]')
        specs = x[1].xpath('./div')[1].xpath('./div/table/tr')
        meta_specifications = {}
        specifications = ''
        for spec in specs:
            for sp in spec.xpath('./td/table/tr'):
                sp = sp.xpath('./td')
                if len(sp) < 2: continue
                xx = sp.xpath('./text()').extract()[0].strip().replace('.', '')
                yy = sp.xpath('./text()').extract()[1].strip()
                meta_specifications[xx] = yy 
                specifications += xx +': ' + yy + ', '
        specifications = specifications.strip().strip(',') + '.'

        descr_h = x[2].xpath('./div')[1].xpath('./div/div/p/strong/text()').extract()
        descr_b = x[2].xpath('./div')[1].xpath('./div/div/p/text()').extract()
        descr_b = [d.strip() for d in descr_b if len(d.strip()) != 0]
        descr = ' '.join(descr_b)

        highlights = x[0].xpath('./div')[1].xpath('./ul/li/span/text()').extract()
        highlights = ', '.join(highlights) + '.'
        return descr, specifications, meta_specifications, highlights 

    def color_func(meta_specs):
        try:
            return meta_specs['Colour']
        except:
            return None

    def brand_func(meta_specs):
        try:
            return meta_specs['Brand']
        except:
            return None

    def group_func(response):
        group = response.xpath('.//div[@id="breadCrumbWrapper2"]/div/a/span/text()').extract()
        group = ', '.join(group)
        return group

    def offer_func(response):
        try:
            offer = response.xpath('.//div[contains(@class, "offer-content")]/div/div/text()').extract()
            offer = [o.strip() for o in offer if len(o.strip())!= 0]
            return ', '.join(offer) + '.'
        except:
            return None

    def instock_func(response):
        try: 
            response.xpath('.//div[@class="sold-out-err"]/text()')[0]
            return 0
        except:
            return 1

    def imageurl_func(response):
        urls = response.xpath('.//img/@src').extract()
        urls = [x for x in urls if 'jpg' in x.lower() or 'png' in x.lower() or 'jpeg' in x.lower()]
        url = urls[0]
        return url

    price, offer_price, discount = prices(response)
    descr, specs, meta_specs, highlights = description_func(response)

    d = {}
    d['id'] = None
    d['name'] = name_func(response)
    d['permalink'] = None 
    d['create_date'] = None
    d['mrp'] = None
    d['price'] = price
    d['offer_price'] = offer_price
    d['discount'] = discount
    d['store_id'] = None
    d['category'] = group_func(response)
    d['category_id'] = None
    d['data_source'] = 'snapdeal.com'
    d['ref_id'] = None
    d['url'] = response.url
    d['image_url'] = imageurl_func(response)
    d['deal_notes'] = None
    d['meta_title'] = d['name']
    d['meta_key'] = None
    d['meta_des'] = meta_specs
    d['size'] = None
    d['size_unit'] = None
    d['features'] = highlights
    d['description'] = descr
    d['key_features'] = highlights
    d['color'] = color_func(meta_specs)
    d['brand'] = brand_func(meta_specs)
    d['specifications'] = specs
    d['offers'] = offer_func(response)
    d['in_stock'] = instock_func(response)
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
    csv_writer(fh, d['id'],d['name'],d['permalink'],d['create_date'],d['mrp'],d['price'],d['offer_price'],d['discount'],\
               d['store_id'],d['category'],d['category_id'],d['data_source'],d['ref_id'],d['url'],d['image_url'],\
               d['description'],d['deal_notes'],\
               d['meta_title'],d['meta_key'],d['meta_des'],d['brand'],d['size'],d['size_unit'],d['color'],d['key_features'],\
               d['features'],d['specifications'],d['offers'],d['in_stock'],d['free_shipping'],d['shippingCharge'],\
               d['mm_average_rating'],d['is_deal'],d['is_coupon'],d['start_date'],d['end_date'],d['coupon_code'],\
               d['special_deal'],d['upcoming_deal'],d['show_as_banner'],d['local_store_deal'],d['localstore_deal_enabled'],\
               d['featured'],d['enabled'],d['no_cashback'],d['base_product'],d['match_set'],d['match_attempt'],d['store_count'],\
               d['display_order'],d['last_update'],d['deleted'])

