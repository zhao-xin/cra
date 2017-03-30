import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
from selenium import webdriver
import sys

wb = Workbook()
ws = wb.active

# driver = webdriver.Chrome('C:\Users\home\PycharmProjects\chromedriver')
driver = webdriver.Chrome('/Users/uqxzhao1/Documents/python/chromedriver')
# driver = webdriver.PhantomJS('/Users/uqxzhao1/Documents/python/phantomjs-2.1.1-macosx/bin/phantomjs')

date = time.strftime("%Y%m%d")
print(date)

baseurl = 'https://shop.coles.com.au/'
urls = {
        '/a/a-national/specials/browse/baby?pageNumber=1': '1',
        '/a/a-national/specials/browse/health-beauty/medicinal?pageNumber=1': 'Medicinal',
        '/a/a-national/specials/browse/health-beauty/dental?pageNumber=1': 'Dental',
        '/a/a-national/specials/browse/pantry/pantry-tea?pageNumber=1':'Tea',
        '/a/a-national/specials/browse/pantry/jams--honey-spreads/honey-3694611?pageNumber=1': 'Honey',
        '/a/a-national/specials/browse/pantry/coffee-3116064?pageNumber=1':'Coffee',
        '/a/a-national/specials/browse/pantry/confectionery?pageNumber=1': 'Confectionery',
        '/a/a-national/everything/browse/pantry/oils-vinegars/oil?pageNumber=1': 'Oil',
        '/a/a-national/everything/browse/pantry/canned-foods--soups-noodles/fish-seafood?pageNumber=1': 'Fish/Seafood'
        }

def getPage(url):
    driver.get(url)
    time.sleep(1)

def getProduct(category):
    soup = BeautifulSoup(driver.page_source, 'xml')
    pages = soup.find_all('div', 'product product-specials')
    for page in pages:
        try:
            brand = page.find('span','product-brand').getText()
            brand = str(brand)
        except:
            print('----------------brand error----------------')
        try:
            name = page.find('span', 'product-name').getText()
            name = str(name)
        except:
            print('----------------name error----------------')
        try:
            size = str(page.find('span','package-size').getText())
        except:
            size = 0
        try:
            qty = str(page.find('span', 'product-qty').getText())
            price = str(page.find('strong', 'product-price').getText())
        except:
            continue
        try:
            saving = str('$'+page.find('span', 'product-saving').getText().split('$')[1].replace('\n',''))
        except:
            saving = 0
        a = page.find('a').get('href')
        print(brand,name,size,qty,price,saving,a)
        ws.append([category, brand, '=HYPERLINK("' + baseurl + a + '","' + name + '")', size, qty, price, saving])

def afterPages(category):
    currentPage = False
    while True:
        soup = BeautifulSoup(driver.page_source, 'xml')
        getProduct(category)

        pages = soup.find_all('li', 'page-number')

        for page in pages:
            a = page.find('a', 'button')
            if a is None:
                currentPage = True
                continue
            else:
                if currentPage:
                    pageNumber = a.getText()
                    link = a.get('href')
                    print(link, pageNumber)
                    getPage(baseurl+link)
                    currentPage = False
                    break
        if currentPage or len(pages) == 0:
            break

def main(argv):
    for url in urls:
        level = urls[url]
        getPage(baseurl + url)
        try:
            driver.find_element_by_css_selector('.button.button-dark').click()
        except:
            print('----------------no need to confirm----------------')

        soup = BeautifulSoup(driver.page_source, 'xml')

        if level.isdigit():
            lis = soup.find_all('li', 'cat-nav-item')

            for li in lis:
                a = li.find('a')
                category = a.getText()
                link = a.get('href')
                try:
                    category = str(category)
                except:  # catch *all* exceptions
                    print('-----------------------------------')
                print(link, category)
                getPage(baseurl + link)
                afterPages(category)

        else:
            afterPages(level)
    wb.save("coles" + date + ".xlsx")

if __name__ == "__main__":
    main(sys.argv)




