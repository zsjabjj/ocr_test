# -*- coding: utf-8 -*-
import os
import requests
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

num = 0

dr = webdriver.Chrome()

dr.maximize_window()

dr.implicitly_wait(5)

url = 'https://passport.ganji.com/register.php'
dr.get(url)
if not os.path.exists('ganji'):
    os.makedirs('ganji')
while num <= 100:
    num += 1
    print(num)
    el_captcha = dr.find_element_by_id('img_phone_checkcode')
    captcha_url = el_captcha.get_attribute('src')
    print(captcha_url)
    data = requests.get(captcha_url, headers=headers)

    image_name = 'ganji' + os.sep + 'numeng.ganji.exp' + str(num) + '.jpg'
    with open(image_name, 'wb') as f:
        f.write(data.content)
    print('save ok')
    el_btn = dr.find_element_by_xpath('//*[@id="checkcode"]/a')
    el_btn.click()