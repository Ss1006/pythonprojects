# -*- coding:utf-8 -*-
import scrapy
from faker import Factory
# from zhihu_spider.items import ZhihuSpiderItem
import urlparse
import requests
from bs4 import BeautifulSoup
f = Factory.create()
session = requests.session()


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allow_domain = 'zhihu.com'
    start_urls = ['https://www.zhihu.com']


    headers = {
        'Accept':'* / *',
        'Accept - Encoding':'gzip, deflate, br',
        'Accept - Language':'zh - CN, zh;q = 0.8',
        'Connection':'keep - alive',
        'Content - Length':92,
        'Content - Type':'application / x - www - form - urlencoded;charset = UTF - 8',
        'Host':'www.zhihu.com',
        'User-Agent': f.user_agent()
    }
    formdata = {
        'password':'Ss1006',
        'captcha_type':'cn',
        'phone_num': '17698955971',
    }

    def start_requests(self):
        return [scrapy.Request(
            url='https://www.zhihu.com/#signin',
            headers=self.headers,
            meta={'cookiejar':1},
            callback = self.parse_login,
        )]

    def parse_login(self,response):
        _xsrf = response.xpath('//div[@class="view view-signin"]/form/input/@value').extract()[0]
        captcha_url = response.xpath('//div[@class="Captcha input-wrapper"]/div[2]/img[@class="Captcha-image"]/@src').extract_first()
        link = 'https://www.zhihu.com'+captcha_url
        r = session.get(link,headers=self.headers)
        with open('captcha.gif','wb') as f:
            f.write(r.content)
            f.close()
        from PIL import Image
        try:
            im = Image.open('captcha.gif')
            im.show()
            im.close()
        except:
            pass
        captcha=input('请输入验证码：')
        return captcha
        captcha = '{"img_size":[200,44],"input_points":[[9.98608,21.0694],[44.9861,25.0694]]}'
        self.formdata['_xsrf'] = _xsrf
        self.formdata['captcha'] = captcha
        self.formdata['captcha_type'] = 'cn'
        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.formdata,
                                                 headers=self.headers,
                                                 meta={'cookiejar':response.meta['cookiejar']},
                                                 callback=self.after_login)]






    def after_login(self,response):
        print response.status







