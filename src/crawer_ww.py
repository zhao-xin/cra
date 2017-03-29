import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
from selenium import webdriver
import sys

wb = Workbook()
ws = wb.active

driver = webdriver.Chrome('C:\Users\home\PycharmProjects\chromedriver')
# driver = webdriver.PhantomJS()

date = time.strftime("%Y%m%d")
print(date)

baseurl = 'https://www.woolworths.com.au'
urls = {'/Shop/SpecialsGroups/health-beauty-sale': 'Health & Beauty',
        '/Shop/SpecialsGroups/baby-sale': 'Baby'}

def main(argv):
    for url in urls:
        level = urls[url]
        driver.get(baseurl + url)

        time.sleep(1)
        for i in range(100):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'xml')
        a = 1

if __name__ == "__main__":
    main(sys.argv)




