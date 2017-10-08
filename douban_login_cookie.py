import requests

headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36  (KHTM, like Gecko/44.0.2403.157 Safari/537.36)'}
cookies = {'cookie':'ue="2319788370@qq.com"; ll="118282"; bid=YTRWJX0K9Bg; ps=y; __yadk_uid=qMCcH4mgdDkbHGPSvEpJpd2yYisaMdKM; _ga=GA1.2.1213896493.1505619396; _gid=GA1.2.1441592307.1505619453; ue="2319788370@qq.com"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1505631445%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%22%5D; __utmt=1; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.8cb4=05b5f4d07338c197.1505619391.3.1505632496.1505629581.; _pk_ses.100001.8cb4=*; __utma=30149280.1213896493.1505619396.1505631446.1505632445.4; __utmb=30149280.6.10.1505632445; __utmc=30149280; __utmz=30149280.1505632445.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6971'}
url = 'http://www.douban.com'
r = requests.get(url,cookies = cookies,headers = headers)
with open('douban_2.txt','wb+') as f:
    f.write(r.content)
