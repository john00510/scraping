from selenium import webdriver
from datetime import datetime
from pymongo import MongoClient
import time, os

def csv_opener(fn):
    path = '/'.join(os.path.abspath('').split('/')[:-3])+'/output/'
    fn = path + fn + '.csv'
    header = 'id,name,permalink,create_date,mrp,price,offer_price,discount,store_id,category_id,\
              data_source,ref_id,url,description,deal_notes,meta_title,meta_key,meta_des,brand,\
              size,size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
              shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
              special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
              featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
              display_order,last_update,deleted\n'

    fh = open(fn, 'w')
    fh.write(header)
    return fh

def log_opener(fn):
    path = '/'.join(os.path.abspath('').split('/')[:-3])+'/logs/'
    fn = path + fn + '.log'
    fh = open(fn, 'w')
    return fh

def log_writer(fh, url, error):
    line = str(error) + ' | ' + url + '\n'
    fh.write(line)

def csv_writer(fh, id, name, permalink, create_date, mrp,price,offer_price,discount,store_id,category_id,\
               data_source,ref_id,url,description,deal_notes,meta_title,meta_key,meta_des,brand, size,\
               size_unit,color,key_features,features,specifications,offers,in_stock,free_shipping,\
               shippingCharge,mm_average_rating,is_deal,is_coupon,start_date,end_date,coupon_code,\
               special_deal,upcoming_deal,show_as_banner,local_store_deal,localstore_deal_enabled,\
               featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,display_order,\
               last_update,deleted):
    name = name.replace('"', '')
    create_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    meta_title = meta_title.replace('"', '')
    meta_des = str(meta_des).replace('"', '')
    specifications = specifications.replace('"', '')
    features = str(features).replace('"', '')
    description = description.replace('"', '')
    line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
           "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
           "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (id,name.replace('"', "'"),permalink,create_date,\
           mrp,price,offer_price,discount,store_id,category_id, data_source,ref_id,url,description,deal_notes,\
           meta_title,meta_key,meta_des.replace('"', "'"),brand, size,size_unit,color,key_features,features,\
           specifications,offers,in_stock,free_shipping,shippingCharge,mm_average_rating,is_deal,is_coupon,\
           start_date,end_date,coupon_code,special_deal,upcoming_deal,show_as_banner,local_store_deal,\
           localstore_deal_enabled,featured,enabled,no_cashback,base_product,match_set,match_attempt,store_count,\
           display_order,last_update,deleted)

    fh.write(line.encode('utf8'))

def selenium_spider(url):
    def proxy_changing():
        proxy_host = '159.203.117.131'
        proxy_port = '3128'
        fp = webdriver.FirefoxProfile()
        fp.set_preference('network.proxy.type', 1)
        fp.set_preference('network.proxy.http', proxy_host)
        fp.set_preference('network.proxy.http_port', int(proxy_port))
        fp.set_preference('network.proxy.https', proxy_host)
        fp.set_preference('network.proxy.https_port', int(proxy_port))
        fp.update_preferences()
        return fp

    def phantomjs_wd():
        driver = webdriver.PhantomJS()
        driver.get(url)
        return driver

    def firefox_wd():
        driver = webdriver.Firefox()
        driver.get(url)
        return driver

    driver = firefox_wd()
    time.sleep(5)
    return driver

def mongo_db():
    client = MongoClient()
    db = client.stores
    coll = db.tatacliq
    return client, coll

def mongo_writer(coll, item):
    try:
        coll.insert(item)
    except Exception, e:
        print str(e)



