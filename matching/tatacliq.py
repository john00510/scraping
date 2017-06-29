import pandas as pd
from pymongo import MongoClient

def tatacliq():
    client = MongoClient()
    db = client.stores
    coll = db.full_collection.find({'source': 'tatacliq.com'})
    df = pd.DataFrame(list(coll))
    df = df.apply(get_lower, axis=1)
    print df['category'].unique()

def get_lower(row):
    try:
        row['brand'] = row['brand'].lower()
        if row['category'] == 'air conditioner':
            row['category'] = 'air conditioners'
        if row['category'] == 'laptop':
            row['category'] = 'laptops'
    except:
        pass
    return row


if __name__ == "__main__":
    tatacliq()

