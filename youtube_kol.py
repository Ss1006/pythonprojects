# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:39:37 2021

@author: 105385
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from lxml import etree
from time import sleep
import requests
import re
import pandas as pd
#实现规避检测
from selenium.webdriver import ChromeOptions


#实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(options=option)



for query in ['creality']:
    url = 'https://www.youtube.com/results?search_query=' + query + '&sp=EgQQARgB'
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    cookie = driver.get_cookies()
    js = "window.scrollBy(0,document.body.scrollHeight)"
    height = 2501
    # height=driver.execute_script('window.scrollBy(0,200000000)')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    
    t1 = int(time.time())
    status=True
    num=0
    n=0
    while status:
        t2=int(time.time())
        if t2-t1 < 30:
              new_height = height*n
              n=n+1
              if new_height > height :
                  time.sleep(1)
                  driver.execute_script('window.scrollBy(%d, %d)'%(height,new_height))
                  # 重置初始页面高度
                  height = new_height
                  # 重置初始时间戳，重新计时
                  t1 = int(time.time())
              elif num < 3:                        # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
                  time.sleep(3)
                  num = num+1
              else:    # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
                  print("滚动条已经处于页面最下方！")
                  status = False
                  # 滚动条调整至页面顶部
                  driver.execute_script('window.scrollTo(0, 0)')
                  break
        



def parse_home_page(driver):
    tree = etree.HTML(driver.page_source)
    video_list = tree.xpath('//div[@id="contents"]/ytd-video-renderer')
    title_list=[]
    video_url_list=[]
    view_times_list=[]
    post_time_list=[]
    author_list=[]
    author_url_list=[]
    like_list=[]
    subscribe_list=[]
    location_list=[]
    for video in video_list:
        title=video.xpath('./div//h3/a/@title')[0]
        video_url='https://www.youtube.com/'+str(video.xpath('./div//h3/a/@href')[0])
        like_count,subscribe_count=parse_video_page(video_url)
        view_times=video.xpath('./div//div[@id="metadata"]/div[2]/span[1]/text()')[0]
        post_time=video.xpath('./div//div[@id="metadata"]/div[2]/span[2]/text()')[0]
        author=video.xpath("./div//yt-formatted-string/a/text()")[0]
        author_url='https://www.youtube.com/'+video.xpath("./div//yt-formatted-string/a/@href")[0]
        adress=parse_author_page(author_url)
        title_list.append(title)
        video_url_list.append(video_url)
        view_times_list.append(view_times)
        post_time_list.append(post_time)
        author_list.append(author)
        author_url_list.append(author_url)
        like_list.append(like_count)
        subscribe_list.append(subscribe_count)
        location_list.append(adress)

        

df=pd.DataFrame({'title':title_list,'video_url':video_url_list,'view_times':view_times_list,
                  'post_time':post_time_list,'author':author_list,'author_url':author_url_list,
                  'like':like_list,'subscribe':subscribe_list,'location':location_list})
df.to_excel(r'D:\work\spider\youtube\youtube_kol_2.xlsx',index=False)
    
def parse_video_page(video_url):       
    response=requests.get(video_url).text
    like_ex='{"iconType":"LIKE"},"defaultText":{"accessibility":{"accessibilityData":{"label":"(.*?) likes"'
    like= re.findall(like_ex,response,re.S)
    if len(like)>0:
        like=like[0]
    else:
        like=0
    subscribe_ex='"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.*?) subscribers"'
    subscribe=re.findall(subscribe_ex,response,re.S)
    if len(subscribe)>0:
        subscribe=subscribe[0]
    else:
        subscribe=0          
    return like,subscribe
    


def parse_author_page(author_url):
    response=requests.get(url=url+'/about').text
    location_ex='"country":{"simpleText":"(.*?)"}'
    location=re.findall(location_ex,response,re.S)
    if len(location)>0:
        location=location[0]
    else:
        location=0 
    return location
            
    