from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import requests
from pyquery import PyQuery as pq

keyword = '美食'
base_url = 'http://weixin.sogou.com/weixin?'
proxy_pool_url = 'http://localhost:5555/random'
proxy = None
max_count = 5

headers = {
    'Cookie':'SUV=1522119703151179; SMYUV=1522119703156558; UM_distinctid=16265677b042f0-044e6f54caf16e-3f3c5906-1fa400-16265677b08e2d; IPLOC=CN4403; SUID=797D253B2F20910A000000005ABA0FA4; pgv_pvi=4442129408; ld=ulllllllll2zmkM6lllllVrjJwDlllllnhqdWyllllwllllllklll5@@@@@@@@@@; LSTMV=168%2C23; LCLKINT=3061; ABTEST=8|1522672804|v1; weixinIndexVisited=1; SUIR=50550D12282D41F5C97B0402297493A3; PHPSESSID=etcrht9g9nch19bfi33reg0mg5; JSESSIONID=aaaaeZJTDuYZldUlSOOiw; sct=13; SNUID=0A0F574973771A1A98ACD28873588A2B; ppinf=5|1523274765|1524484365|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTMlODElQUYlRTMlODElOEYlRTMlODIlODR8Y3J0OjEwOjE1MjMyNzQ3NjV8cmVmbmljazoyNzolRTMlODElQUYlRTMlODElOEYlRTMlODIlODR8dXNlcmlkOjQ0Om85dDJsdUFMSVVfNmkwbU1sWE9lNENfTzRIREFAd2VpeGluLnNvaHUuY29tfA; pprdig=UaZxLqhW29dysA-LKuYdO9aQIMK91BdvHLujvkp3zvsc5w_QMOcJLuXj1TWYIp9alBNBIqCeHFjUa6BLBj7u4dKM3NUvGLwj03qZgPkNN0tK9ILw7nI4DW2vrdJa-z7u5xv03IJiNKVsDdWfQg4uhDojQ-SMZb4Gr4sWxhTGRyo; sgid=03-32373271-AVrLVA3iaTwFa03luZjwdVdI; ppmdig=1523274765000000a3a0bc2f00fa1666e02df512ac4cd7f9',
    'Host':'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/weixin?query=%E6%9D%AD%E5%B7%9E&type=2&page=8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None



def get_html(url,count = 1):
    print('Crawling',url)
    print('Trying count',count)
    global proxy
    if count >= max_count:
        print('Trying Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http':'http://'+ proxy
            }
            response = requests.get(url,allow_redirects = False,headers = headers,proxies = proxies)
        else:
            response = requests.get(url, allow_redirects = False,headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy',proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Erroe occured',e.args)
        proxy = get_proxy()
        count +=1
        return get_html(url,count)

def get_index(keyword,page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    url = base_url + urlencode(data)
    html = get_html(url)

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    date = doc('#post-date').text()
    nickname = doc('#js_profile_qrcode > div > strong').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    content = doc('rich_media_content ').text().strip()
    return{
        'title':title,
        'date':date,
        'nickname':nickname,
        'wechat':wechat,
        'content':content
    }


def main():
    for page in range(1,101):
        html = get_index(keyword,page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)



if __name__ == '__main__':
    main()
