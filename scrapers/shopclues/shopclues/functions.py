import re
from com_functions import csv_writer

def shopclues_item_parser(response, fh):
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
        try:
            color = response.xpath('.//li[@scname="Colour"]/div')
        except:
            color = ''
        return color

    def brand_func(meta_specs):
        try:
            brand = meta_specs['Brand']
        except:
            brand = ''
        return brand

    def group_func(response):
        try:
            group = response.xpath('.//div[@id="breadCrumbWrapper2"]/div/a/span/text()').extract()
            group = ', '.join(group)
        except:
            group = ''
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

    price, offer_price, discount = prices_func(response)
    meta_specs, specs = specs_func(response)

    id = ''
    name = name_func(response)
    permalink = '' 
    create_date = ''
    mrp = ''
    price = price
    offer_price = offer_price
    discount = discount
    store_id = ''
    category_id = ''#group_func(response)
    data_source = 'shopclues.com'
    ref_id = prod_id_func(response)
    url = response.url
    deal_notes = ''
    meta_title = name
    meta_key = ''
    meta_des = meta_specs
    size = ''
    size_unit = ''
    features = specs
    description = specs
    key_features = ''#highlights
    color = color_func(response)
    brand = brand_func(meta_specs)
    specifications = specs
    offers = offer_func(response)
    in_stock = ''#instock_func(response)
    free_shipping = shipping_func(response)
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
    csv_writer(fh,id,name,permalink,create_date,mrp,price,offer_price,discount,store_id,category_id,\
               data_source,ref_id,url,description,deal_notes,meta_title,meta_key,meta_des,brand,\
               size,size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
               shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
               special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
               featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
               display_order,last_update,deleted)



