from selenium import webdriver
from datetime import datetime
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
import time, os

def csv_opener(fn):
    path = '/'.join(os.path.abspath('').split('/')[:-3])+'/output/tatacliq/'
    fn = path + fn + '.csv'
    header = 'name,permalink,create_date,mrp,price,offer_price,discount,store_id,category,category_id,\
              source,data_source,ref_id,url,image_url,description,deal_notes,meta_title,meta_key,meta_des,brand,\
              size,size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
              shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
              special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
              featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
              display_order,last_update,deleted\n'

    fh = open(fn, 'w')
    fh.write(header)
    return fh

def csv_writer(fh, name, permalink, create_date, mrp,price,offer_price,discount,store_id,category,category_id,\
               source,data_source,ref_id,url,image_url,description,deal_notes,meta_title,meta_key,meta_des,brand, size,\
               size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
               shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
               special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
               featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,display_order,\
               last_update,deleted):
    name = name.replace('"', '')
    create_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    meta_title = name
    meta_des = name
    features = str(features).replace('"', '')
    description = description.replace('"', '')
    line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
           "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
           "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (name,permalink,create_date,\
           mrp,price,offer_price,discount,store_id,category,category_id,source,data_source,ref_id,url,image_url,description,deal_notes,\
           meta_title,meta_key,meta_des,brand, size,size_unit,color,key_features,features,\
           specifications,offers,in_stock,free_shipping,shippingCharge,mm_average_rating,is_deal,is_coupon,\
           start_date,end_date,coupon_code,special_deal,upcoming_deal,show_as_banner,local_store_deal,\
           localstore_deal_enabled,featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
           display_order,last_update,deleted)

    fh.write(line.encode('utf8'))

def chrome_spider(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)
    return driver

def mongo_open(coll_name):
    client = MongoClient()
    db = client.stores
    coll = db[coll_name]
    return client, coll

def mongo_write(coll, item):
    try:
        coll.insert(item)
    except Exception, e:
        if 'E11000 duplicate key error' in str(e):
            pass
        else:
            print str(e)
            #print item
            raise e

