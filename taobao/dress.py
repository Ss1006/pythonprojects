# -*- coding:utf-8 -*-
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo


from project.taobao.config import MONGO_DB, MONGO_URL, MONGO_TABLE

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
driver = webdriver.Chrome()
driver.get("https://www.taobao.com/")
wait = WebDriverWait(driver, 10)
def search():
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_TSearchForm > div.search-button")))
        input.send_keys("连衣裙")
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.total")))
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.send_keys(page_num)
        submit.click()
        num = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_num)))
        get_products()
    except TimeoutException:
        return next_page(page_num)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)
def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range( 2 ,total + 1):
        next_page(i)
    driver.close()

if __name__ =='__main__':
    main()