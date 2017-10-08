import requests
from PIL import Image
from io import BytesIO
import json

# print(dir(requests))

# url = 'http://www.baidu.com'
# r = requests.get(url)
# # print (r)
#
# params = {'k1':'v1','k2':[1,2,3]}
# r = requests.get('http://httpbin.org/get',params)
# print(r.url)


# r = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1505620336264&di=fca0a98076e0772f163e28fd572cf0c4&imgtype=0&src=http%3A%2F%2F4493bz.1985t.com%2Fuploads%2Fallimg%2F140828%2F4-140RQ35130.jpg')
# image = Image.open(BytesIO(r.content))
# image.save('meinv.jpg')

# r = requests.get('https://github.com/timeline.json')
# print(type(r.json))
# print(r.text)
#
# r = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1505620336264&di=fca0a98076e0772f163e28fd572cf0c4&imgtype=0&src=http%3A%2F%2F4493bz.1985t.com%2Fuploads%2Fallimg%2F140828%2F4-140RQ35130.jpg',stream = True)
# with open('meinv2.jpg','wb+') as f:
#     for chunk in r.iter_content(1024):
#         f.write(chunk)

#提交表单
# form = {'username':'name','password':'pass'}
# r = requests.post('http://httpbin.org/post',data=form)
# print(r.text)
# r = requests.post('http://httpbin.org/post',data=json.dumps(form))
# print(r.text)

# cookie
# url = 'http://www.baidu.com'
# r = requests.get(url)
# cookies = r.cookies
# for k,v in cookies.get_dict().items():
#     print(k,v)
# cookies = {'c1':'v1','c2':'v2'}
# r = requests.post('http://httpbin.org/cookies',cookies = cookies)
# print(r.text)

#重定向
r = requests.get('https://github.com',allow_redirects = True )
print(r.url)
print(r.status_code)
print(r.history)

#代理
proxies = {'http':'...','https':'...'}
r = requests.get('...',proxies = proxies)




