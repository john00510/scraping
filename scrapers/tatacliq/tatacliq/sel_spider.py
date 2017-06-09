from com_functions import selenium_spider
import time, re

def cats_func(url):
    driver = selenium_spider(url)
    #cats = driver.find_elements_by_xpath('.//ul[@class="shopByDepartment_ajax"]/li')
    cats = driver.find_elements_by_xpath('.//div[@class="toggle L2"]/a')
    for cat in cats:
        print cat.text

    driver.quit()

def item_number(url):
    driver = selenium_spider(url)
    nums = driver.find_elements_by_xpath('.//div[@id="categoryPageDeptHierTree"]/ul/li/ul/li/ul/li')
    summ = 0
    for num in nums:
        num = num.find_elements_by_xpath('./div/span')[1].text
        num = re.findall(r'([0-9]+)', num)[0]
        summ += int(num)
  
    driver.quit()
    pgs = summ / 24 + 5
    return summ, pgs

urls = [
'https://www.tatacliq.com/electronics-tablets/c-msh1211', # 300
'https://www.tatacliq.com/electronics-mobile-phones/c-msh1210/', # 1500
'https://www.tatacliq.com/electronics-tv/c-msh1216',
'https://www.tatacliq.com/electronics-large-appliances/c-msh1214',
'https://www.tatacliq.com/electronics-air-conditioner/c-msh1230',
'https://www.tatacliq.com/electronics-wearable-devices/c-msh1219',
'https://www.tatacliq.com/electronics-camera/c-msh1220',
'https://www.tatacliq.com/electronics-laptop/c-msh1223',
'https://www.tatacliq.com/electronics-kitchen-appliances/c-msh1229',
'https://www.tatacliq.com/electronics-small-appliances/c-msh1231',
'https://www.tatacliq.com/electronics-personal-care/c-msh1236',
'https://www.tatacliq.com/electronics-storage-devices/c-msh1228',
#'https://www.tatacliq.com/electronics-accessories/c-msh1222',
]

def main():
    fh = open('urls.py', 'w')
    fh.write('urls = [\n')
    for url in urls:
        d = {}
        summ, pgs = item_number(url)
        d['url'] = url
        d['items'] = summ
        d['pages'] = pgs
        line = '%s,\n' % str(d)
        fh.write(line)

    fh.write(']')
    fh.close()

main()


