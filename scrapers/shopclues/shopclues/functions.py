import re
from com_functions import csv_writer, mongo_writer

def shopclues_item_parser(response, fh, coll):
    def name_func(response):
        return response.xpath('.//h1[@itemprop="name"]/text()').extract()[0].strip()

    def prod_id_func(response):
        try:
            prod_id = response.xpath('.//span[@class="pID"]/text()').extract()[0]
            return re.findall(r'([0-9]+)', prod_id)[0]
        except:
            return None

    def prices_func(response):
        try:
            price = response.xpath('.//div[@class="price"]/span[@itemprop="highPrice"]/@content').extract()[0]
            offer_price = response.xpath('.//div[@class="price"]/span[@itemprop="lowPrice"]/@content').extract()[0]
            discount = response.xpath('.//div[@class="price"]/span[@itemprop="offerCount"]/text()').extract()[0].split(' ')[0]
        except:
            try:
                price = response.xpath('.//div[@class="price"]/span[@itemprop="lowPrice"]/@content').extract()[0]
                offer_price = price
                discount = None
            except:
                price = None
                offer_price = None
                discount = None
        return price, offer_price, discount

    def shipping_func(response):
        ship = response.xpath('.//li[@id="shippingcharge"]/text()').extract()
        if 'Free Shipping' in ship:
            return 1
        else:
            return 0

    def specs_func(response):
        try:
            specs = response.xpath('.//div[@id="specification"]/table/tbody/tr')
            d = {}
            l = ''
            for sp in specs:
                s = sp.xpath('./td/span/text()').extract()
                if len(s) ==0: continue
                d[s[0]] = s[1]
                l += s[0] + ': ' + s[1] + '; '
            l = l.strip().strip(';') + '.'
        except:
            print 'error'
            d = ''
            l = ''
        return d, l

    def color_func(response):
        color = response.xpath('.//li[@scname="Color"]/span/text()').extract()
        return ', '.join(color)

    def brand_func(meta_specs):
        try:
            return meta_specs['Brand']
        except:
            return None

    def group_func(response):
        group = response.xpath('.//div[@class="breadcrums"]/ul/li/a/span/text()').extract()[1:]
        return ', '.join(group)

    def offer_func(response):
        try:
            offer = response.xpath('.//ul[@id="promo_offr"]/li/text()').extract()
            offer = [o.strip() for o in offer if len(o.strip())!= 0]
            return '. '.join(offer) + '.'
        except:
            return None

    def instock_func(response):
        try: 
            response.xpath('.//div[@class="sold-out-err"]/text()')[0]
            return 0
        except:
            return 1

    def image_func(response):
        images = response.xpath('.//img/@src').extract()
        images = [i for i in images if 'logo' not in i]
        return [i for i in images if len(i.strip()) != 0][0]

    def descr_func(response):
        descr = response.xpath('.//div[@id="product_description"]/p/span/text()').extract()
        pass

    price, offer_price, discount = prices_func(response)
    meta_specs, specs = specs_func(response)

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
    d['data_source'] = 'shopclues.com'
    d['ref_id'] = prod_id_func(response)
    d['url'] = response.url
    d['image_url'] = image_func(response)
    d['deal_notes'] = None
    d['meta_title'] = d['name']
    d['meta_key'] = None
    d['meta_des'] = meta_specs
    d['size'] = None
    d['size_unit'] = None
    d['features'] = specs
    d['description'] = specs
    d['key_features'] = None #highlights
    d['color'] = color_func(response)
    d['brand'] = brand_func(meta_specs)
    d['specifications'] = specs
    d['offers'] = offer_func(response)
    d['in_stock'] = None #instock_func(response)
    d['free_shipping'] = shipping_func(response)
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

