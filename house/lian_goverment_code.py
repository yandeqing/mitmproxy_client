#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/2/8 10:28
'''
import requests

from utils import time_util


def print_header(response):
    print(f"{response.url}")
    print(f"==response headers==========================")
    items = response.headers.items()
    for item in items:
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")


def house_list(page=1,limit=30):
    ts = time_util.now_to_timestamp()
    url = f"https://wx-api.zu.ke.com/v1/house/list?city_id=310000&limit={limit}&scene=home&page_uicode=matrix_homepage&from=default_list&condition=ab200301001000&offset={limit*page}&feed_query_id=2080341113113&ts={ts}"

    payload = {}
    headers = {
        'Host': 'wx-api.zu.ke.com',
        'Connection': 'keep-alive',
        'Cookie': 'zf_token=;lianjia_token=;lianjia_uuid=a66827a6-34f4-7ee2-a375-cfc4a144fbf0;lianjia_udid=oYveJ5bAL_bW8OsYZAGrdwbjT1rI;rent_uuid=a4bf4a84-7d58-4c79-bcf5-9036041670db;; lianjia_ssid=f6c2c99d-58d8-4740-bf29-9d01d5fdc5a6; lianjia_uuid=a3ecccb4-5301-495c-a029-1d7c6d755aba',
        'LIANJIA-VERSION': '1.11.0',
        'Lianjia-Access-Token': '',
        'Lianjia-City-Id': '310000',
        'Page-Schema': 'subpackages/rent/pages/index/index',
        'RENT-APP-ID': 'rent-xcx',
        'RENT-SIGN': '009a6302b5326fef02507c2d15f31afe',
        'RENT-VERSION': '1.11.0',
        'Rent-User-Agent': 'wx-grid',
        'UA': 'wx-grid',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Xcx-Referer': '',
        'Xcx-Version': '9.24.2',
        'beikeBaseData': '{"openid":"oYveJ5bAL_bW8OsYZAGrdwbjT1rI"}',
        'content-type': 'application/json',
        'parentSceneId': '',
        'Referer': 'https://servicewechat.com/wxcfd8224218167d98/292/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    response = requests.get(url, headers=headers, data=payload)
    print_header(response)
    json = response.json()
    print(json)
    return json


def house_detail(house_code="SH1571798624143147008"):

    ts = time_util.now_to_timestamp()
    url = f"https://wx-api.zu.ke.com/v1/house/detail?house_code={house_code}&invite_ucid=0&ts={ts}"

    payload = {}
    headers = {
        'Host': 'wx-api.zu.ke.com',
        'Connection': 'keep-alive',
        'Cookie': 'zf_token=;lianjia_token=;lianjia_uuid=fc5a19b7-5a1c-c9d1-a6a2-725fa464b485;lianjia_udid=oYveJ5bAL_bW8OsYZAGrdwbjT1rI;rent_uuid=a4bf4a84-7d58-4c79-bcf5-9036041670db;; lianjia_ssid=ab1314f3-d2fe-430c-a2b9-e2e96b2e4d11',
        'LIANJIA-VERSION': '1.11.0',
        'Lianjia-Access-Token': '',
        'Lianjia-City-Id': '310000',
        'Page-Schema': 'subpackages/rent/pages/detail/index',
        'RENT-APP-ID': 'rent-xcx',
        'RENT-SIGN': '0889e86a471a00b7bedbdbeb23fdfc9b',
        'RENT-VERSION': '1.11.0',
        'Rent-User-Agent': 'wx-grid',
        'UA': 'wx-grid',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Xcx-Referer': 'subpackages/rent/pages/detail/index',
        'Xcx-Version': '9.24.2',
        'beikeBaseData': '{"openid":"oYveJ5bAL_bW8OsYZAGrdwbjT1rI"}',
        'content-type': 'application/json',
        'parentSceneId': '5963590585604909312',
        'Referer': 'https://servicewechat.com/wxcfd8224218167d98/292/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    response = requests.get(url, headers=headers, data=payload)

    print_header(response)
    json = response.json()
    print(json)
    return json


if __name__ == '__main__':
    house_detail()
    # house_list()
