import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

date = time.strftime("%Y%m%d")
print(date)

baseurl = 'https://www.chemistwarehouse.com.au'
url = baseurl + '/categories'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
trs = soup.find_all('tr')

category1 = ''
category2 = ''
category3 = ''

def process_page(link):
    print(category1, category2, category3)
    # return
    while True:
        page = requests.get(baseurl+link)
        soup = BeautifulSoup(page.text, 'lxml')

        products = soup.find_all('a', 'product-container')
        for prod in products:
            href = prod.get('href')
            text = prod['title']
            try:
                text = str(text)
            except:  # catch *all* exceptions
                print('-----------------------------------')
            price = str(prod.find('span','Price').getText().split()[0])
            save = prod.find('span','Save')
            if save is None:
                save = 0
            else:
                save = str(save.getText().split()[1])
            print(category1, category2, category3, text, price, save)

            ws.append([category1, category2, category3, '=HYPERLINK("'+baseurl+href+'","'+text+'")', price, save])

        a = soup.find('a', 'next-page')
        if a is not None:
            next = a.get('href')
            if next != link:
                link = next
                continue
        break

for tr in trs:
    img = tr.find('img')
    if img is None:
        continue
    tds = tr.find_all('td')
    if len(tds) < 3 or len(tds) > 5:
        continue

    span = tr.find('span', 'CategoryTreeItem')
    if span is None:
        continue
    category = span.getText()
    a = span.find('a')
    link = a.get('href')
    try:
        category = str(category)
    except:  # catch *all* exceptions
        print('-----------------------------------')

    if len(tds) == 3:
        if (category2 != 'N/A' and category3 == 'N/A') or (category1 != 'N/A' and category2 == 'N/A'):
            process_page(linkPerious)
        category1 = category
        category2 = 'N/A'
        category3 = 'N/A'
        linkPerious = link

    if len(tds) == 4:
        if category2 != 'N/A' and category3 == 'N/A':
            process_page(linkPerious)
        category2 = category
        category3 = 'N/A'
        linkPerious = link

    if len(tds) == 5:
        category3 = category
        process_page(link)
        linkPerious = ''

if linkPerious != '':
    process_page(linkPerious)

wb.save("cw"+date+".xlsx")


