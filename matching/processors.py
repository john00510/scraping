from pymongo import MongoClient
import pandas as pd
import os

def open_mongo(collection, source):
    client = MongoClient()
    db = client.stores
    coll = db[collection]
    mongo_df = coll.find({'source': source})
    df = pd.DataFrame(list(mongo_df))
    return df


def flipkart():
    total = pd.DataFrame()
    path = os.path.abspath('output/flipkart/')
    files = os.listdir(path)

    for f in files[:]:
        ppath = '%s/%s' % (path, f)
        df = pd.read_csv(ppath)
        total = total.append(df)

    total = total.rename(columns = {'productBrand': 'brand', 'title': 'name', 'categories': 'category'})
    return total

def open_csv(df):
    if df == 'tatacliq':
        path = os.path.abspath('output/matching_tatacliq.csv')
        fh = open(path, 'w')
        header = 'tatacliq,amazon,ebay\n'
        fh.write(header)
        return fh   

    if df == 'amazon':
        path = os.path.abspath('output/matching_amazon.csv')
        fh = open(path, 'w')
        header = 'amazon,tatacliq,ebay\n'
        fh.write(header)
        return fh  

    if df == 'total':
        path = os.path.abspath('output/matching_total.csv')
        fh = open(path, 'w')
        header = 'tatacliq,amazon,ebay\n'
        fh.write(header)
        return fh  

def write_csv(df, fh, dfn):
    if dfn == 'tatacliq':
        for index, row in df.iterrows():
            line = '"%s","%s","%s"\n' % (row['name'].replace('"', ' '), row['amazon'].replace('"', ' '), row['ebay'].replace('"', ' '))
            fh.write(line.encode('utf8'))

    if dfn == 'amazon':
        for index, row in df.iterrows():
            try:
                name2 = row['tatacliq'].replace('"', ' ')
            except:
                name2 = row['tatacliq'] 

            try:
                name3 = row['ebay'].replace('"', ' ')
            except:
                name3 = row['ebay'] 

            line = '"%s","%s","%s"\n' % (row['name'].replace('"', ' '), name2, name3)
            fh.write(line.encode('utf8'))

    if dfn == 'total':
        for index, row in df.iterrows():
            try:
                name2 = row['amazon'].replace('"', ' ')
            except:
                name2 = row['amazon'] 

            try:
                name3 = row['ebay'].replace('"', ' ')
            except:
                name3 = row['ebay'] 

            line = '"%s","%s","%s"\n' % (row['name'].replace('"', ' '), name2, name3)
            fh.write(line.encode('utf8'))


