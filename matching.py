#encoding: utf8
import pandas as pd
from pymongo import MongoClient
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os


def amazon():
    client = MongoClient()
    db = client.stores
    coll = db.amazon
    mongo_df = coll.find()
    pd_df = pd.DataFrame(list(mongo_df))
    pd_df.name = 'amazon'
    return pd_df

def ebay():
    client = MongoClient()
    db = client.stores
    coll = db.ebay
    mongo_df = coll.find()
    pd_df = pd.DataFrame(list(mongo_df))
    pd_df.name = 'ebay'
    return pd_df

def flipkart():
    total = pd.DataFrame()
    path = os.path.abspath('output/flipkart/')
    files = os.listdir(path)
    for f in files[:]:
        ppath = '%s/%s' % (path, f)
        df = pd.read_csv(ppath)
        total = total.append(df)
    total = total.drop_duplicates()
    total.name = 'flipkart'
    return total

def tatacliq():
    client = MongoClient()
    db = client.stores
    coll = db.tatacliq
    mongo_df = coll.find()
    pd_df = pd.DataFrame(list(mongo_df))
    pd_df.name = 'tatacliq'
    return pd_df

def snapdeal():
    client = MongoClient()
    db = client.stores
    coll = db.snapdeal
    mongo_df = coll.find()
    pd_df = pd.DataFrame(list(mongo_df))
    pd_df.name = 'snapdeal'
    return pd_df

def shopclues():
    client = MongoClient()
    db = client.stores
    coll = db.shopclues
    mongo_df = coll.find()
    pd_df = pd.DataFrame(list(mongo_df))
    pd_df.name = 'shopclues'
    return pd_df

def groupby1(df1, df2):
    colors = df1['color'].drop_duplicates()
    brands = df1['brand'].drop_duplicates()
    for x in colors:
        if len(x) == 0: continue
        if '-' in x: continue
        for y in brands:
            if len(y) == 0: continue
            if '-' in y: continue
            color = x.lower()
            brand = y.lower()
            print x, y
            df1.groupby('color')

def groupby2(df1, df2):
    for group, frame in ta.groupby('color'):
        if len(group) == 0 or '-' in group: 
            continue
        for groupp, framee in frame.groupby('brand'):
            if len(groupp) == 0 or '-' in groupp: 
                continue
            print framee.columns

def filter_df(li):
    li = [(l, len(l)) for l in li]
    li.sort()
    return li[-1]

def open_csv():
    path = os.path.abspath('output/matching_results/matching_results.csv')
    fh = open(path, 'w')
    header = 'tatacliq,amazon,score\n'
    fh.write(header)
    return fh    

def main():

    #ta_df = ta_df[ta_df['category_id'] == 'Mobile Phones']

    #print len(am_df), len(ta_df)

    #results_df = ta_df.apply(lambda x: matching(x, am_df, fh), axis=1)

    '''for x, y, z in results_df.iterrows():
        line = '"%s","%s","%s"\n' % (x.replace('"', ''), y.replace('"', ''), z.replace('"', ''))
        fh.write(line.encode('utf8'))'''

    #fh.close()

def matching(row, match_df, fh):
    row['amazon_name'], row['score'] = process.extractOne(row['name'], match_df['name'], scorer=fuzz.ratio) # token_sort_ratio, partial_ratio
    line = '"%s","%s","%s"\n' % (row['name'], row['amazon_name'], row['score'])
    fh.write(line.encode('utf8'))
    print row['name']
    print row['amazon_name']
    print '#######################################'


if __name__ == '__main__':
    ta = tatacliq()
    #eb = ebay()
    #sn = snapdeal()
    #fl = flipkart()
    #sh = shopclues()
    am = amazon()

    #groupby2(am, ta)
    #for group, frame in ta.groupby('brand'):
    #    print group
    #print len(ta[ta['brand'] == 'Vivo'])
    taa = ta.where(ta['brand'] == 'Vivo')
    #ta = ta[ta['color'] == 'Navy']
    print len(taa)





