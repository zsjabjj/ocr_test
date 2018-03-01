# -*- coding: utf-8 -*-
import pytesseract
import requests
from PIL import Image
from selenium import webdriver

class Douban(object):
    def __init__(self):
        self.url = 'https://www.douban.com/'

        self.dr = webdriver.Chrome()
        self.dr.maximize_window()

        self.dr.implicitly_wait(10)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        pass

    def __del__(self):
        self.dr.close()

    def get_captcha(self):
        captcha_url = self.dr.find_element_by_id('captcha_image').get_attribute('src')
        data = requests.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(data.content)


    def run(self):
        self.dr.get(self.url)
        # 定位节点
        email_input = self.dr.find_element_by_id('form_email')
        email_input.send_keys('')
        pwd_input = self.dr.find_element_by_id('form_password')
        pwd_input.send_keys('')
        # 获取验证码图片
        self.get_captcha()
        im = Image.open('captcha.jpg')
        print(pytesseract.image_to_string(im))
        pass


if __name__ == '__main__':
    douban = Douban()
    douban.run()
