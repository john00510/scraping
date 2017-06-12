import re
from com_functions import csv_writer, mongo_writer

def shopclues_item_parser(response, fh, coll):
    def name_func(response):
        try:
            name = response.xpath('.//h1[@itemprop="name"]/text()').extract()[0].strip()
        except:
            name = ''
        return name

    def prod_id_func(response):
        try:
            prod_id = response.xpath('.//span[@class="pID"]/text()').extract()[0]
            prod_id = re.findall(r'([0-9]+)', prod_id)[0]
        except:
            prod_id = ''
        return prod_id

    def prices_func(response):
        try:
            price = response.xpath('.//div[@class="price"]/span[@itemprop="highPrice"]/@content').extract()[0]
            offer_price = response.xpath('.//div[@class="price"]/span[@itemprop="lowPrice"]/@content').extract()[0]
            discount = response.xpath('.//div[@class="price"]/span[@itemprop="offerCount"]/text()').extract()[0].split(' ')[0]
        except:
            try:
                price = response.xpath('.//div[@class="price"]/span[@itemprop="lowPrice"]/@content').extract()[0]
                offer_price = price
                discount = ''
            except:
                price = ''
                offer_price = ''
                discount = ''
        return price, offer_price, discount

    def shipping_func(response):
        ship = response.xpath('.//li[@id="shippingcharge"]/text()').extract()
        if 'Free Shipping' in ship:
            shipping = 1
        else:
            shipping = 0
        return shipping

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
        color = ', '.join(color)
        return color

    def brand_func(meta_specs):
        try:
            brand = meta_specs['Brand']
        except:
            brand = ''
        return brand

    def group_func(response):
        group = response.xpath('.//div[@class="breadcrums"]/ul/li/a/span/text()').extract()[1:]
        group = ', '.join(group)
        return group

    def offer_func(response):
        try:
            offer = response.xpath('.//ul[@id="promo_offr"]/li/text()').extract()
            offer = [o.strip() for o in offer if len(o.strip())!= 0]
            offer = '. '.join(offer) + '.'
        except:
            offer = ''
        return offer

    def instock_func(response):
        try: 
            response.xpath('.//div[@class="sold-out-err"]/text()')[0]
            in_stock = 0
        except:
            in_stock =1
        return in_stock

    def image_func(response):
        images = response.xpath('.//img/@src').extract()
        images = [i for i in images if 'logo' not in i]
        image = [i for i in images if len(i.strip()) != 0][0]
        return image

    def descr_func(response):
        descr = response.xpath('.//div[@id="product_description"]/p/span/text()').extract()
        pass

    price, offer_price, discount = prices_func(response)
    meta_specs, specs = specs_func(response)

    d = {}
    d['id'] = ''
    d['name'] = name_func(response)
    d['permalink'] = '' 
    d['create_date'] = ''
    d['mrp'] = ''
    d['price'] = price
    d['offer_price'] = offer_price
    d['discount'] = discount
    d['store_id'] = ''
    d['category_id'] = group_func(response)
    d['data_source'] = 'shopclues.com'
    d['ref_id'] = prod_id_func(response)
    d['url'] = response.url
    d['image_url'] = image_func(response)
    d['deal_notes'] = ''
    d['meta_title'] = d['name']
    d['meta_key'] = ''
    d['meta_des'] = meta_specs
    d['size'] = ''
    d['size_unit'] = ''
    d['features'] = specs
    d['description'] = specs
    d['key_features'] = ''#highlights
    d['color'] = color_func(response)
    d['brand'] = brand_func(meta_specs)
    d['specifications'] = specs
    d['offers'] = offer_func(response)
    d['in_stock'] = ''#instock_func(response)
    d['free_shipping'] = shipping_func(response)
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
    mongo_writer(coll, d)
    csv_writer(fh, d['id'],d['name'],d['permalink'],d['create_date'],d['mrp'],d['price'],d['offer_price'],d['discount'],\
               d['store_id'],d['category_id'],d['data_source'],d['ref_id'],d['url'],d['image_url'],d['description'],d['deal_notes'],\
               d['meta_title'],d['meta_key'],d['meta_des'],d['brand'],d['size'],d['size_unit'],d['color'],d['key_features'],\
               d['features'],d['specifications'],d['offers'],d['in_stock'],d['free_shipping'],d['shippingCharge'],\
               d['mm_average_rating'],d['is_deal'],d['is_coupon'],d['start_date'],d['end_date'],d['coupon_code'],\
               d['special_deal'],d['upcoming_deal'],d['show_as_banner'],d['local_store_deal'],d['localstore_deal_enabled'],\
               d['featured'],d['enabled'],d['no_cashback'],d['base_product'],d['match_set'],d['match_attempt'],d['store_count'],\
               d['display_order'],d['last_update'],d['deleted'])

