import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.set_page_load_timeout(30)

browser.get('http://www.17huo.com/search.html?sq=2&keyword=%E5%A4%A7%E8%A1%A3')
page_info = browser.find_element_by_css_selector('body > div.wrap > div.pagem.product_list_pager > div')

pages =int((page_info.text.split(', ')[0]).split(' ')[1])
print('商品有%d页' % pages)
for i in range(pages):
    if i > 5:
        break
    print('第%d页' % (i+1))
    url = 'http://www.17huo.com/?mod=search&sq=2&keyword=大衣&page='+str(i)
    browser.get(url)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(3)
    goods = browser.find_element_by_css_selector('body > div.wrap > div:nth-child(2) > div.p_main > ul').find_elements_by_tag_name('li')
    print('第%d页有%d件商品' % ((i + 1),len(goods)))
    for good in goods:
        try:
            title = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(2)').text
            price = good.find_element_by_css_selector('div > span').text
            print(title ,price)
        except:
            print('Exception')