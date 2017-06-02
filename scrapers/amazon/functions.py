from com_functions import mongo_writer, csv_writer
from datetime import datetime

def item_parsing(item):
    d = {}
    d['id'] = ''
    d['name'] = item['productBaseInfoV1']['title']
    d['permalink'] = '' 
    d['create_date'] = ''
    d['mrp'] = ''
    d['price'] = ''
    d['offer_price'] = '' 
    d['discount'] = ''
    d['store_id'] = ''
    d['category_id'] = '' 
    d['data_source'] = 'flipkart.com'
    d['ref_id'] = ''
    d['url'] = ''
    d['description'] = '' 
    d['deal_notes'] = ''
    d['meta_title'] = ''
    d['meta_key'] = ''
    d['meta_des'] = ''
    d['brand'] = ''
    d['size'] = ''
    d['size_unit'] = ''
    d['key_features'] = ''
    d['features'] = ''
    d['color'] = ''
    d['specifications'] = ''
    d['offers'] = ''
    d['in_stock'] = ''
    d['free_shipping'] = ''
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

