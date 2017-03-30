#coding:utf-8
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class seleniumTest(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome('C:\Users\home\PycharmProjects\chromedriver')
        # self.driver = webdriver.Chrome('/Users/uqxzhao1/Documents/python/chromedriver')
        self.driver = webdriver.PhantomJS('/Users/uqxzhao1/Documents/python/phantomjs-2.1.1-macosx/bin/phantomjs')
    def testEle(self):
        driver = self.driver
        driver.get('http://www.douyu.com/directory/all')
        soup = BeautifulSoup(driver.page_source, 'xml')
        while True:
            titles = soup.find_all('h3', {'class': 'ellipsis'})
            nums = soup.find_all('span', {'class': 'dy-num fr'})
            for title, num in zip(titles, nums):
                print(title.get_text(), num.get_text())
            if driver.page_source.find('shark-pager-disable-next') != -1:
                break
            elem = driver.find_element_by_class_name('shark-pager-next')
            elem.click()
            soup = BeautifulSoup(driver.page_source, 'xml')

    def testScroll(self):
        driver = self.driver
        driver.get('http://www.jianshu.com/collections')
        time.sleep(1)
        for i in range(10):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1)

    def tearDown(self):
        print('down')

if __name__ == "__main__":
    unittest.main()