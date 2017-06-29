import pandas as pd
import os
from flipkart_stop_list import stop_list

global stop_list


def flipkart():
    total = pd.DataFrame()
    path = '/home/john/Scripts/upwork_projects/scraping/output/flipkart/'
    files = os.listdir(path)

    for f in files[:]:
        ppath = '%s/%s' % (path, f)
        df = pd.read_csv(ppath)
        total = total.append(df)

    total = total[~total['categories'].isin(stop_list)].rename(columns={'title': 'name', 'productUrl': 'url', 'imageUrlStr': 'image_url', 'productBrand': 'brand', 'categories': 'category'})
    #total = total[~total.name.str.contains('Screen Guard')]
    #total = total[~total.name.str.contains('Glass Guard')]
    #total = total[~total.name.str.contains('Front & Back Protector')]

    total = total.apply(df_filter, axis=1)

    #for group, frame in total.groupby('brand'):
    #    print group, len(frame)
    return total

def df_filter(row):
    row['brand'] = row['brand'].lower()
    try:
        if 'Tablets' in row['category']:
            row['category'] = 'tablets'
        if 'Handsets' in row['category']:
            row['category'] = 'mobile phones'
        if 'Laptops' in row['category']:
            row['category'] = 'laptops'
        if 'Cameras' in row['category']:
            row['category'] = 'cameras'
        if 'Wearable Smart Devices' in row['category']:
            row['category'] = 'wearable devices'
        if 'Air Conditioners' in row['category']:
            row['category'] = 'air conditioners'
        if 'Air Coolers' in row['category']:
            row['category'] = 'air conditioners'
        if 'Refrigerators' in row['category']:
            row['category'] = 'large appliances'
        if 'Washing Machines & Dryers' in row['category']:
            row['category'] = 'large appliances'
        if 'Kitchen Appliances' in row['category']:
            row['category'] = 'kitchen appliances'
        if 'TV & Video' in row['category']:
            row['category'] = 'tv'
    except:
        pass
    return row

    
if __name__ == "__main__":
    flipkart()

