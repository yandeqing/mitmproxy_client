#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/15 16:14
'''
import json

import requests

from js import JsUtil


def print_response(response):
    print(f"url========={response.url}")
    print(f"status_code={response.status_code}")
    response.encoding = "gbk"
    print(f"cookies======{response.cookies}=====")
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    print(f"response content========={response.text}")


url = "http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/1/ajax/1/free/1/"
js = "https://s.thsi.cn/js/chameleon/chameleon.min.1642236.js"

if __name__ == '__main__':
    v = JsUtil.getV()
    headers = {
        "Host": "data.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "image/avif,image/webp,*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Referer": "http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/1/ajax/1/free/1/",
        "Cookie": f"v={v}",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    print(f"=====url={url}=====")
    jsons = json.dumps(headers, indent=4, ensure_ascii=False)
    print(f"headers={jsons}")
    session = requests.session()
    response = session.get(url, headers=headers, data={}, allow_redirects=True)
    # session.cookies.save()
    print_response(response)
