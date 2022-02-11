#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/2/8 10:28
'''
import requests


def print_header(response):
    print(f"{response.url}")
    print(f"==response headers==========================")
    items = response.headers.items()
    for item in items:
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")


def house_list(page=1):
    url = "https://appapi.5i5j.com/appapi/renting/9/v1/list"
    payload = f'government=1&pcount=50&page={page}&source=3&broom=&buildarea=&communityid=&decoratetype=&floortype=&heading=&keywords=&location=&nearby=&othertype=&price=&renttype=&districtids=&sqids=&lineid=&stationid=&tags=&psort=&lift=&heatingType=&buildType='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'devicesource': '3',
        'deviceid': '47133882-db22-4c14-a196-0b21765eedaa',
        'recommendgiodeviceid': '47133882-db22-4c14-a196-0b21765eedaa',
        'smdeviceid': 'WHJMrwNw1k/EYw46DTtpFeUaQi1NIMDJggpqmkJBV32eHJ8DUKiJp+kMxPk7RvXkXLwo+sfZHnB4BQlcbnyj6XO6R73dC8jtpdCW1tldyDzmauSxIJm5Txg==1487582755342',
        'referer': 'https://servicewechat.com/wxaf705dee544e08d9/527/page-frame.html',
        'accept-encoding': 'gzip, deflate, br',
        'Cookie': 'PHPSESSID=o12ntmseqmino2q8abhi4o4m4b'
    }
    response = requests.post(url, headers=headers, data=payload)
    print_header(response)
    json = response.json()
    print(json)
    return json


def house_detail(hid="45722747"):
    url = "https://appapi.5i5j.com/appapi/renting/9/v1/detail"
    payload = f'hid={hid}&source=3&portLocation=3'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'devicesource': '3',
        'deviceid': '47133882-db22-4c14-a196-0b21765eedaa',
        'recommendgiodeviceid': '47133882-db22-4c14-a196-0b21765eedaa',
        'smdeviceid': 'WHJMrwNw1k/EYw46DTtpFeUaQi1NIMDJggpqmkJBV32eHJ8DUKiJp+kMxPk7RvXkXLwo+sfZHnB4BQlcbnyj6XO6R73dC8jtpdCW1tldyDzmauSxIJm5Txg==1487582755342',
        'referer': 'https://servicewechat.com/wxaf705dee544e08d9/527/page-frame.html',
        'accept-encoding': 'gzip, deflate, br',
        'Cookie': 'PHPSESSID=o12ntmseqmino2q8abhi4o4m4b'
    }
    response = requests.post(url, headers=headers, data=payload)
    print_header(response)
    json = response.json()
    print(json)
    return json


if __name__ == '__main__':
    house_list()
    # house_detail()
