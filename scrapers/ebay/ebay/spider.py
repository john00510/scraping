#encoding: utf-8
import requests, time, re
from lxml import html
from com_functions import mongo_open, mongo_write
from urls import urls


def get_category(url, coll):
    for url in urls:
        page1 = url['first_url']
        page2 = url['second_url']
        category = url['category'].lower()
        itms = 50
        r1 = requests.get(
            page1, 
            headers={
                'referer': 'http://www.ebay.in',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
            },
        )
        itemss = get_items(r1.content, coll, category)
        print '%s, page 1, scraped %s items' % (category, itemss)
        page = 2

        while True:
            u = re.sub(r'skc=50&', 'skc=%s&', re.sub(r'pgn=2&', 'pgn=%s&', page2) % page) % itms
            r2 = requests.get(
                u, 
                headers={
                    'referer': 'http://www.ebay.in',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
                },
            )
            items = get_items(r2.content, coll, category)

            if items == 0:
                break

            print '%s, page %s, scraped %s items' % (category, page, items)
            itms += 50
            page += 1
            time.sleep(1)

def get_items(response, coll, category):
    tree = html.fromstring(response)
    items = tree.xpath('.//ul[@id="ListViewInner"]/li[contains(@id, "item")]')
    for item in items:
        d = {}
        d['url'] = item.xpath('.//h3/a/@href')[0]
        d['name'] = item.xpath('.//h3/a/text()')[0].strip().replace('"', ' ')
        d['category'] = category
        d['source'] = 'ebay.in'
        mongo_write(coll, d)

    return len(items)


if __name__ == '__main__':
    client, coll = mongo_open('short_collection')
    get_category(urls, coll)
    client.close()

