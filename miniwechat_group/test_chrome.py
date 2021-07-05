#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/27 17:00
'''
from selenium import webdriver

opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--headless')
opt.add_argument('blink-settings=imagesEnabled=false')
opt.add_argument('--disable-gpu')
browser = webdriver.Chrome('/opt/google/chromedriver',chrome_options=opt)
browser.get('http://www.baidu.com/')
print(browser.title)