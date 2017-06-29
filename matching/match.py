#!/usr/bin/python
#encoding: utf8
import pandas as pd
from fuzzywuzzy import fuzz, process
from processors import open_mongo, open_csv, write_csv
from flipkart import flipkart
from tatacliq import tatacliq


def groupby(df, list1):
    ndf = pd.DataFrame()
    for group, frame in df.groupby(['category', 'brand']):
        category, brand = group
        ndf = ndf.append(frame.apply(lambda x: match(x, list1, category, brand), axis=1))
        print brand, len(frame) #, [len(l[l['category'] == category][l['brand'] == brand]) for l in list1]
  
    return ndf

def match(row, li, category, brand):
    for l in li:
        filt = l[l['category'] == category][l['brand'] == brand]
        try:
            name, score = process.extractOne(row['name'], filt['name'], scorer=fuzz.token_sort_ratio)
            col_name = filt.iloc[0]['source'].split('.')[0]
            if score > 60:
                row[col_name] = name
            else:
                row[col_name] = None
        except:
            pass
    return row


if __name__ == '__main__':
    #global fh_am

    #ta = open_mongo('short_collection', 'tatacliq.com').drop_duplicates('name')
    #am = open_mongo('short_collection', 'amazon.in').drop_duplicates('name')
    #eb = open_mongo('full_collection', 'ebay.in').drop_duplicates('name')

    flipkart = groupby(flipkart(), [tatacliq(), ebay()])
    #write_csv(amazon, fh_am, 'amazon')

    #list2 = [eb]
    #amazon = groupby(am, list2)
    #write_csv(amazon, fh_am, 'amazon')

    #total = pd.merge(tatacliq, amazon, how='outer', left_on='amazon', right_on='name')
    #print total.columns
    #write_csv(total, fh_tot, 'total')

    #fh_ta.close()
    #fh_am.close()
    #fh_tot.close()

