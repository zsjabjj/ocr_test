# -*- coding: utf-8 -*-
import json

import requests
import os
from selenium import webdriver


class Panda(object):
    def __init__(self):
        # 构建url
        self.url = 'https://www.panda.tv'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        # 创建浏览器对象
        self.dr = webdriver.Chrome()
        self.dr.maximize_window()

        # 缓冲时间
        # self.dr.implicitly_wait(10)

        self.data_list = list()
        # self.temp = dict()

        # 保存文件
        self.f = open('panda.json', 'w', encoding='UTF-8')

    def __del__(self):
        self.f.close()
        # self.dr.close()

    def parse_data(self):
        # //*[@id="list-top"]/li/a  五条
        # //*[@id="list-content"]/li/a  57条
        # 定位到大范围节点

        print('星颜页面定位节点开始')
        list_top = self.dr.find_elements_by_xpath('//*[@id="list-top"]/li/a')
        print('list_top')

        print('start temp')
        for lp in list_top:
            temp = dict()
            temp['link'] = lp.get_attribute('href')
            temp['address'] = lp.find_element_by_xpath('./span').text
            temp['title'] = lp.find_element_by_xpath('./div[2]/span[1]').text
            temp['image_url'] = 'https:' + lp.find_element_by_xpath('./div[1]/img').get_attribute('data-original')
            temp['uname'] = lp.find_element_by_xpath('./div[2]/div/span[2]').text
            temp['hot'] = lp.find_element_by_xpath('./div[2]/span[2]').text
            self.data_list.append(temp)
        list_content = self.dr.find_elements_by_xpath('//*[@id="list-content"]/li/a')
        print('list_content')
        for lc in list_content:
            temp = dict()
            temp['link'] = lc.get_attribute('href')
            temp['address'] = lc.find_element_by_xpath('./span').text
            temp['title'] = lc.find_element_by_xpath('./div[2]/span[1]').get_attribute('title')
            temp['image_url'] = 'https:' + lc.find_element_by_xpath('./div[1]/img').get_attribute('data-original')
            temp['uname'] = lc.find_element_by_xpath('./div[2]/div/span[2]').text
            temp['hot'] = lc.find_element_by_xpath('./div[2]/span[2]').text
            # print(self.temp)
            self.data_list.append(temp)

    def save_data(self):
        for data in self.data_list:
            str_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.f.write(str_data)

    def down_image(self):
        num = 0
        if not os.path.exists('images'):
            os.makedirs('images')

        for data in self.data_list:
            print(data)
            url = data['image_url']
            print(url)
            if data['uname']:
                filename = 'images' + os.sep + data['uname'] + '.jpeg'
            else:
                filename = 'images' + os.sep + str(num + 1) + '.jpeg'
            with open(filename, 'wb') as f:
                f.write(requests.get(url, headers=self.headers).content)

    def run(self):
        # 请求页面
        print('开始请求页面')
        self.dr.get(self.url)
        self.dr.implicitly_wait(10)
        # 点击分类
        print('选择分类')
        el_kind = self.dr.find_element_by_xpath('//*[@id="panda_header"]/div/div/div[2]/ul/li[3]/a')
        el_kind.click()
        self.dr.implicitly_wait(10)
        # 点击星颜分类
        print('选择星颜')
        el_xingyan = self.dr.find_element_by_xpath('//*[@id="main-container"]/div[2]/ul/li[6]/a')
        el_xingyan.click()
        # 获取所有窗口句柄
        handle_list = self.dr.window_handles
        print(handle_list)
        # 切换到星颜窗口
        print('切换到星颜窗口')
        self.dr.switch_to.window(handle_list[-1])
        print(self.dr.current_window_handle)
        self.dr.implicitly_wait(10)
        # 获取数据并解析
        print('获取并解析数据开始')
        self.parse_data()
        # 保存数据
        print('save data')
        self.save_data()
        # 保存图片
        print('save image')
        self.down_image()


if __name__ == '__main__':
    panda = Panda()
    panda.run()
