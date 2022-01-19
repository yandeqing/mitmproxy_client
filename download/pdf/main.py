#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/17 12:54
'''
import requests

from utils import re_util, csv_util, FilePathUtil, time_util


def get_examination_materials():
    i = 1
    arr_all = []
    while True:
        url = f"http://m.hqwx.com/ziliao/class_zqcy/?pageNo={i}"
        response = requests.get(url)
        if response and response.text:
            print(response.text)
            arr = re_util.find_texts_by_reg(r'data-url="(.+?\.pdf)', response.text)
            if len(arr) == 0:
                print(f"===已完成{i}==")
                break
            else:
                arr_all.extend(arr)
            i = i + 1
    f = open(f'{FilePathUtil.get_full_dir("download", "pdf", "考试资料.txt")}', "a+", encoding="utf-8")
    for item in arr_all:
        print(item)
        f.write(item + "\n")
    f.close()


def get_recent_practise_materials(url):
    arr_all = []
    response = requests.get(url)
    if response and response.text:
        print(response.text)
        arr = re_util.find_texts_by_reg(r'data-url="(.+?\.pdf)', response.text)
        if arr:
            arr_all.extend(arr)
    date = time_util.now_to_date("%Y-%m-%d")
    f = open(f'{FilePathUtil.get_full_dir("download", "pdf", f"{date}资料.txt")}', "a+", encoding="utf-8")
    for item in arr_all:
        print(item)
        f.write(item + "\n")
    f.close()


if __name__ == '__main__':
    url = f"http://m.hqwx.com/news/2022-1/16417784982588.html"
    get_recent_practise_materials(url)
