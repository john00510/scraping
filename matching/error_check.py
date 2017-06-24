import pandas as pd
from processors import open_mongo

am = open_mongo('short_collection', 'amazon.in')


for group, frame in am.groupby(['category', 'brand']):
    print group, len(frame)
