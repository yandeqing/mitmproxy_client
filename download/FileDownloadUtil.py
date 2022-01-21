#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/21 13:14
'''
import os
import time

import requests


def downloadFile(localpath, remote_url):
    print(f"localpath={localpath}")
    print(f"remote_url={remote_url}")
    headers = {'Proxy-Connection': 'keep-alive'}
    r = requests.get(remote_url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open(localpath, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 1:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                print(f'已下载 {formatFloat(p)}% (下载速度:{formatFloat(speed)}M/s)')
                time1 = time.time()
    print(f'已下载 {formatFloat(100)}%')
    f.close()

def formatFloat(num):
    return '{:.2f}'.format(num)

if __name__ == '__main__':
    downloadFile("1.pdf","https://oss-hqwx-video.hqwx.com/2021年12月12日证券从业资格《金融市场基础知识》考试真题及答案_e0a6fc1080efc603de0b943b5f878fb103a75ae0.pdf")