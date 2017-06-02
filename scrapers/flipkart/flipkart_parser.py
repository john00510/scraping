import requests, json
from flipkart_groups import groups
from functions import item_parsing
from com_functions import csv_opener, mongo_db, log_func


_id = 'dealsmera'
token = '062f272c28a0482495fbcaa22980e368'
group_url = "https://affiliate-api.flipkart.net/affiliate/api/" + _id + ".json"

def request(url, _id, token):
    r = requests.get(
        url,
        headers={
            'Fk-Affiliate-Id': _id,
            'Fk-Affiliate-Token': token,
        }
    )
    return r

def group_parser(fh, coll, fhl):
    r = request(group_url, _id, token)
    obj = r.json()['apiGroups']['affiliate']['apiListings']
    for k, v in obj.iteritems():
        if v['apiName'] not in groups: continue
        print k
        item_url = v['availableVariants']['v1.1.0']['get']
        list_parser(item_url, fh, coll, fhl)

def list_parser(url, fh, coll, fhl):
    while True:
        if url == None: break
        r = request(url, _id, token)
        obj = r.json()
        items = obj['productInfoList']
        items_parser(items, fh, coll, fhl)
        url = obj['nextUrl']

def items_parser(items, fh, coll, fhl):
    for item in items:
        item_parsing(item, fh, coll, fhl)


def main():
    fh = csv_opener('flipkart')
    fhl = log_func('flipkart')
    cl, coll = mongo_db()
    group_parser(fh, coll, fhl)
    fh.close()
    cl.close()
    fhl.close()

main()
