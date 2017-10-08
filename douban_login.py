import requests
import re
import html5lib
from bs4 import BeautifulSoup

s = requests.session()
url_login = 'https://accounts.douban.com/login'
url_contacts = 'https://www.douban.com/people/****/contacts'

formdata = {
    'redir':'https://www.douban.com',
    'form_email':'2319788370@qq.com',
    'form_password':'Ss19911006',
    'login': u'登录'
}
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36  (KHTM, like Gecko/44.0.2403.157 Safari/537.36)'}
r = requests.post(url_login,data=formdata,headers = headers)
content = r.text
soup = BeautifulSoup(content,'html5lib')
captcha =soup.find('img',id = 'captcha_image')
if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type ="hidden" name="captcha_id" value="(.*?)"/'
    captcha_id = re.findall(re_captcha_id,content)
    print(captcha_id)
    print(captcha_url)
    captcha_text = input('Please input the captcha:')
    formdata['captcha-solution'] = captcha_text
    formdata['captcha-id'] = captcha_id
    r = s.post(url_login,data=formdata,headers=headers)
r = s.get(url_contacts)
with open('contacts.txt','w+',encoding='utf-8') as f:
    f.write(r.text)