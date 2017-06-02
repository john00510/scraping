import requests

Access_Key_ID = 'AKIAJGZDFG2JNM3M47HA'
Secret_Access_Key = '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'
AssociateTag = 'meradeals08-21'

u_url = 'http://webservices.amazon.in/onca/xml?Service=AWSECommerceService&Operation=ItemSearch&SubscriptionId=AKIAJGZDFG2JNM3M47HA&AssociateTag=meradeals08-21 &SearchIndex=All&Keywords=Air Conditioner&ResponseGroup=Accessories,Images,ItemAttributes,ItemIds,Large,OfferFull,OfferListings,Offers'

s_url = 'http://webservices.amazon.in/onca/xml?AWSAccessKeyId=AKIAJGZDFG2JNM3M47HA&AssociateTag=meradeals08-21%20&Keywords=Air%20Conditioner&Operation=ItemSearch&ResponseGroup=Accessories%2CImages%2CItemAttributes%2CItemIds%2CLarge%2COfferFull%2COfferListings%2COffers&SearchIndex=All&Service=AWSECommerceService&Timestamp=2017-04-22T09%3A45%3A47.000Z&Signature=LhvUwcKZCw8cy%2FK64c0zqra9cxMNec2ZPEyD%2Fd%2Be5ls%3D'

def req(url):
    r = requests.get(
        url,
    )
    return r

def main():
    with open('amazon_unsinged.xml', 'w') as fh:
        r = req(u_url)
        print r
        print >> fh, r
        fh.close()

main()

