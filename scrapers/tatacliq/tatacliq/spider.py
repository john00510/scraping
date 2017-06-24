#encoding: utf-8
import requests, urlparse, time
from lxml import html
from com_functions import mongo_open, mongo_write


urls = [
#'https://www.tatacliq.com/electronics-tablets/c-msh1211', # 300
'https://www.tatacliq.com/electronics-mobile-phones/c-msh1210/', # 1500
#'https://www.tatacliq.com/electronics-tv/c-msh1216',
#'https://www.tatacliq.com/electronics-large-appliances/c-msh1214',
#'https://www.tatacliq.com/electronics-air-conditioner/c-msh1230',
#'https://www.tatacliq.com/electronics-wearable-devices/c-msh1219',
#'https://www.tatacliq.com/electronics-camera/c-msh1220',
#'https://www.tatacliq.com/electronics-laptop/c-msh1223',
#'https://www.tatacliq.com/electronics-kitchen-appliances/c-msh1229',
#'https://www.tatacliq.com/electronics-small-appliances/c-msh1231',
#'https://www.tatacliq.com/electronics-personal-care/c-msh1236',
#'https://www.tatacliq.com/electronics-storage-devices/c-msh1228',
#'https://www.tatacliq.com/electronics-accessories/c-msh1222',
]

def get_categories(urls, coll):
    for url in urls:
        get_category(url, coll)

def get_category(url, coll):
    count = 1
    while True:
        u = url + 'page-%s/' % count
        r = requests.get(
            u,
            headers={
                'referer': 'https://www.tatacliq.com/', 
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
            },
        ) 
        time.sleep(1)
        items = get_items(r.content, count, coll)
        if items == 0:
            break

        print 'page %s, scraped %s items' % (count, items)

        count += 1
        
def get_items(response, count, coll):
    tree = html.fromstring(response)
    items = tree.xpath('.//li[@class="product-item"]')
    for item in items:
        d = {}
        d['url'] = urlparse.urljoin('https://www.tatacliq.com', item.xpath('.//h2/a/@href')[0])
        d['name'] = item.xpath('.//div[@class="image"]/a/@title')[0].strip()
        d['brand'] = item.xpath('.//div[@class="brand"]/text()')[0].strip().lower()
        d['category'] = 'mobile phones'
        d['source'] = 'tatacliq.com'
        #image_url
        #new_price 
        #old_price
        #discount
        #instock
        mongo_write(coll, d)
    return len(items)



if __name__ == '__main__':
    client, coll = mongo_open('short_collection')
    get_categories(urls, coll)
    client.close()


