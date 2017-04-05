import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
from selenium import webdriver
import sys
import re

wb = Workbook()
ws = wb.active

# driver = webdriver.Chrome('C:\Users\home\PycharmProjects\chromedriver')
driver = webdriver.Chrome('/Users/uqxzhao1/Documents/python/chromedriver')
# driver = webdriver.PhantomJS('/Users/uqxzhao1/Documents/python/phantomjs-2.1.1-macosx/bin/phantomjs')

date = time.strftime("%Y%m%d")
print(date)

baseurl = 'https://www.woolworths.com.au'
urls = {
    '/Shop/BrowseSpecials/baby/baby-nappies-nappy-pants': '1',
    '/Shop/Browse/toiletries-beauty-health-wellbeing/health-supplements': '1',
    '/Shop/Browse/spreads-breakfast-baking-desserts/honey': '0'
        }

def nextPage():
    soup = BeautifulSoup(driver.page_source, 'xml')
    next = soup.find('a', 'paging-next')
    if next is None:
        return None
    else:
        return next.get('href')

def getPage(url):
    driver.get(url)
    time.sleep(1)

def getProduct(category):
    soup = BeautifulSoup(driver.page_source, 'xml')
    div = soup.find('div', attrs={'class': re.compile(r".*\bcardList-cards\b.*")})
    if div is None:
        return
    prods = div.find_all('div','shelfProductStamp-content row')
    for prod in prods:
        try:
            name = prod.find('span', 'shelfProductStamp-productDetailsLink').getText()
            name = str(name)
        except:
            print('----------------name error----------------')
        try:
            size = str(prod.find('span', 'shelfProductStamp-productDetailsPackageSize').getText())
        except:
            size = 0
        try:
            qty = '1'
            price = str(prod.find('span', 'pricingContainer-priceAmount').getText())
        except:
            continue
        try:
            saving = str(prod.find('span', 'pricingContainer-savePrice').getText())
        except:
            saving = 0
        a = prod.find('a').get('href')
        print(name, size, qty, price, saving, a)
        ws.append([category, '=HYPERLINK("' + baseurl + a + '","' + name + '")', size, qty, price, saving])

def main(argv):
    for url in urls:
        getPage(baseurl + url)
        soup = BeautifulSoup(driver.page_source, 'xml')

        level = urls[url]
        if level == '1':
            lis = soup.find_all('a',attrs={'class': re.compile(r".*\bcategoryList-aisle\b.*")})
            for li in lis:
                a = li
                category = a.getText()
                link = a.get('href')
                try:
                    category = str(category)
                except:  # catch *all* exceptions
                    print('-----------------------------------')
                print(link, category)
                getPage(baseurl + link)

                while True:
                    getProduct(category)
                    next = nextPage()
                    if next is None:
                        break
                    print(baseurl + link + next)
                    getPage(baseurl + link + next)
        else:
            while True:
                getProduct(category)
                next = nextPage()
                if next is None:
                    break
                print(baseurl + link + next)
                getPage(baseurl + link + next)

    wb.save("woolworths" + date + ".xlsx")

if __name__ == "__main__":
    main(sys.argv)




