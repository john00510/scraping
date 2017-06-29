import requests, json, zipfile, StringIO, os, datetime, re
from flipkart_groups import groups
from functions import item_parsing
from com_functions import csv_opener, mongo_db, log_func
import pandas as pd


_id = 'dealsmera'
token = '062f272c28a0482495fbcaa22980e368'
#group_url = "https://affiliate-api.flipkart.net/affiliate/api/" + _id + ".json"
group_url = "https://affiliate-api.flipkart.net/affiliate/download/feeds/" + _id + ".json"
path = '/'.join(os.path.abspath('').split('/')[:-2]) + '/output/flipkart/'

def request(url, _id, token):
    r = requests.get(
        url,
        headers={
            'Fk-Affiliate-Id': _id,
            'Fk-Affiliate-Token': token,
        }
    )
    return r

def group_parser():
    r = request(group_url, _id, token)
    obj = r.json()['apiGroups']['affiliate']['apiListings']
    for k, v in obj.iteritems():
        if v['apiName'] not in groups: continue
        item_url = v['availableVariants']['v1.1.0']['get']
        r = request(item_url, _id, token)
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        z.extractall(path)

def csv_conn():
    #date = datetime.datetime.now().strftime('%Y_%m_%d')
    fn = 'flipkart.csv'
    f = open(path+fn, 'w')
    files = os.listdir(path)
    total = len(files)
    count = 0
    for fi in files[:1]:
        count += 1
        print 'total: %s, processed: %s' % (total, count)
        fn = path + fi
        df = pd.read_csv(fn)
        #fh = open(path+fi)
        #for l in fh:
        #    print re.findall(r',(http:.+),', l)
    f.close()


if __name__ == '__main__':
    group_parser()
    #csv_conn()


