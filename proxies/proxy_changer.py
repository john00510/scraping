#path = '/'.join(os.path.abspath('').split('/')[:-3])+'/spiders/proxies.txt'
#path_n = '/'.join(os.path.abspath('').split('/')[:-3])+'/spiders/proxiess.txt'

fh = open('proxies.txt)
fh_2 = open('proxiess.txt', 'w')

for l in fh:
    l = 'http://' + l
    fh_2.write(l)

fh_2.close()
