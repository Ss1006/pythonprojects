from urllib.parse import urlencode
from hashlib import md5
import os
from pyquery import PyQuery as pq
import requests
import json
import re
from json.decoder import JSONDecodeError
from config import *
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]


offset = 0
def get_index(offset,KEYWORD):
    base_url = 'https://www.toutiao.com/search_content/?'
    data = {
        'offset': 0,
        'format': 'json',
        'keyword': KEYWORD,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from':'gallery'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    url = base_url + urlencode(data)
    response = requests.get(url,headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            item_id =item.get('group_id')
            yield 'https://www.toutiao.com/a'+item_id+'/'



def get_detail(url):
    headers ={
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None



def parse_detail(html,url):
    doc = pq(html)
    title = doc('title').text()
    print(title)

    pattern = re.compile('(?<=gallery: JSON.parse\().*"(?=\)\,)',re.S|re.M)
    result = re.search(pattern,html).group()
    if result:
        try:
            data = json.loads(json.loads(result))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                for image in images:download_image(image)
                return{
                    'url':url,
                    'title':title,
                    'images':images
                }
        except JSONDecodeError:
            return None


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

def download_image(url):
    print('正在下载',url)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        print('请求图片出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_index(offset,KEYWORD)
    for url in parse_index(html):
        html = get_detail(url)
        if html:
            result = parse_detail(html,url)
            if result: save_to_mongo(result)



if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main,groups)