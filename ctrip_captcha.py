# -*- coding: utf-8 -*-
# 携程是滑块解锁
import requests
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

num = 0

dr = webdriver.Chrome()

dr.maximize_window()

dr.implicitly_wait(5)

url = 'https://passport.ctrip.com/user/reg/home'
dr.get(url)

while num <= 100:
    num += 1
    print(num)
    el_captcha = dr.find_element_by_id('captcha_image')
    captcha_url = el_captcha.get_attribute('src')
    print(captcha_url)
    data = requests.get(captcha_url, headers=headers)

    image_name = str(num) + '.jpg'
    with open(image_name, 'wb') as f:
        f.write(data.content)

    el_captcha.click()