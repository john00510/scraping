path = '/home/john/Scripts/upwork_projects/scraping/spiders/proxies.txt'
path_n = '/home/john/Scripts/upwork_projects/scraping/spiders/proxiess.txt'

fh = open(path)
fh_2 = open(path_n, 'w')

for l in fh:
    l = 'http://' + l
    fh_2.write(l)

fh_2.close()
