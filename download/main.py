#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/17 12:54
'''
import os

import requests

from download import FileDownloadUtil
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
    date = time_util.now_to_date("%Y-%m-%d")
    f = open(f'{FilePathUtil.get_full_dir("download", "pdf", f"考试资料{date}.txt")}', "a+",
             encoding="utf-8")
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
    f = open(f'{FilePathUtil.get_full_dir("download", "pdf", f"{date}资料.txt")}', "a+",
             encoding="utf-8")
    for item in arr_all:
        print(item)
        f.write(item + "\n")
    f.close()


def download(remote_url=None):
    name = get_name(remote_url)
    local = FilePathUtil.get_or_create_full_dir("download", "pdf", f"{name}")
    FileDownloadUtil.downloadFile(local, remote_url)


def get_name(name):
    arr = re_util.find_texts_by_reg(r'com/(.+?.pdf)', name.strip())
    return arr[0] if arr else None

def get_dir_list(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        print(len(files))  # 当前路径下所有非目录子文件
        return files

if __name__ == '__main__':
    local = FilePathUtil.get_full_dir("download", "pdf")
    get_dir_list(local)
    local = FilePathUtil.get_full_dir("download", "考试资料2022-01-21.txt")
    f = open(local, 'r', encoding="utf-8")
    lines = f.readlines()
    for index,line in enumerate(lines):
        print(f"【line{index}={line}】")
        # download(line.strip())
    f.close()

