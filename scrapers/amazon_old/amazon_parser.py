import requests, os, hmac, hashlib, base64, datetime, time
from time import strftime



url = 'http://webservices.amazon.in/onca/xml'
Service = 'AWSECommerceService'
AssociateTag = 'meradeals08-21'
Operation = 'ItemSearch'
ResponseGroup = 'Accessories%2CImages%2CItemAttributes%2CItemIds%2CLarge%2COfferFull%2COfferListings%2COffers'
SubscriptionId = 'AKIAJGZDFG2JNM3M47HA'
Secret_Access_Key = '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'
SearchIndex = 'All'
Keywords = 'Air%20Conditioner'



path = '/'.join(os.path.abspath('').split('/')[:-2]) + '/output/amazon/'

u_url = 'http://webservices.amazon.in/onca/xml?Service=AWSECommerceService&Operation=ItemSearch&SubscriptionId=AKIAJGZDFG2JNM3M47HA&AssociateTag=meradeals08-21&SearchIndex=All&ResponseGroup=Accessories,Images,ItemAttributes,ItemIds,Large,OfferFull,OfferListings,Offers&Keywords=Air Conditioner'


def req(url):
    r = requests.get(
        url,
    )
    return r

def timestamp():
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return timestamp

def sign(timestamp):
    s = 'AWSAccessKeyId=???&Actor=Johnny%20Depp&AssociateTag=???&Operation=???&ResponseGroup=???&SearchIndex=???&Service=???&Sort=salesrank&Timestamp=???&Version=2013-08-01'
    string_to_sign = 'GET\nwebservices.amazon.in\n/onca/xml\n%s' % s
    h = hmac.new(Secret_Access_Key, string_to_sign, hashlib.sha256)
    sig = base64.b64encode(h.digest())
    return sig

def scraping_pages():
    TimeStamp = timestamp()
    Signature = sign(TimeStamp)
    s_url = '%s?AWSAccessKeyId=%s&AssociateTag=%s&Keywords=%s&Operation=%s&ResponseGroup=%s&SearchIndex=%s&Service=%s&Timestamp=%s&Signature=%s' % (url, SubscriptionId, AssociateTag, Keywords, Operation, ResponseGroup, SearchIndex, Service, TimeStamp, Signature)
    with open(path + '%s.xml' % Keywords, 'w') as fh:
        r = req(s_url)
        print r.content
        print >> fh, r.content
        fh.close()

def main():
    scraping_pages()

main()
