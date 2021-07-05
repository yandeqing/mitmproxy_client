#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/3/29 14:23
'''
import random
from time import sleep

import requests

from utils import csv_util, time_util, re_util
from utils.csv_util import ENCODING_GBK

headers = {
    'x-phone-userid': '4036f61e48cb94bc3a506581cdf47205',
    'Content-Type': 'application/json',
    'referer': 'https://servicewechat.com/wxd7c50643b1190826/13/page-frame.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'
}
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}


def get_road(road):
    url = "https://homestay.jhdz66.com/MobileService/Dic/complementRoad"
    payload = {
        "keyword": road,
        "page": 1,
        "rows": 0
    }
    print(f"【get_road().payload={payload}】")
    response = requests.request("POST", url, headers=headers, json=payload)
    response_json = response.json()
    print(response_json)
    datas_ = response_json['data']
    print(f"{road}共计:{len(datas_)}")
    return datas_


def get_gate(gate='', roadCode="000249"):
    import requests
    url = "https://homestay.jhdz66.com/MobileService/Dic/complementGate"
    payload = {
        "keyword": gate,
        "roadCode": roadCode,
        "page": 1,
        "rows": 0
    }
    print(f"【get_gate().payload={payload}】")
    response = requests.request("POST", url, headers=headers, json=payload)
    json = response.json()
    print(json)
    datas_ = json['data']
    print(f"{roadCode}共计:{len(datas_)}")
    return datas_


def get_house(keyword="上海市静安区长寿路999弄29号", gateCode="310002490009990000000000290000"):
    import requests
    url = "https://homestay.jhdz66.com/MobileService/Dic/complementHouse"
    payload = {
        "keyword": keyword,
        "gateCode": gateCode,
        "page": 1,
        "rows": 0
    }
    print(f"【get_house().payload={payload}】")
    response = requests.request("POST", url, headers=headers, json=payload)
    response_json = response.json()
    print(response_json)
    datas_ = response_json['data']
    print(f"{gateCode}共计:{len(datas_)}")
    return datas_


def save(path, array, force=False):
    keys = csv_util.get_head_from_arr(array)
    print(f"【main().keys={keys}】")
    csv_util.create_csv(path, keys, force=force)
    csv_util.append_csv(path, array)


def batch_getroads(path='dict_department_road_name.csv'):
    array = csv_util.read_csv2array(path)
    last_index = -1
    length = len(array)
    for index, item in enumerate(array):
        name_ = item['road_name']
        if '圆明园路' in name_:
            last_index = index
        #
    for index, item in enumerate(array[last_index + 1:length]):
        randint = random.randint(0, 2)
        print(f"【().sleep={randint}】")
        sleep(randint)
        name_ = item['road_name']
        print(f"【({index}).index={name_}】")
        road_items = get_road(name_)
        if road_items:
            date = time_util.now_to_date("%Y-%m-%d")
            path = f'{date}_road.csv'
            save(path, road_items)


def batch_getgates():
    road_items = csv_util.read_csv2array("2021-03-29_road.csv")
    # 存储道路号信息
    for road_item in road_items:
        roadCode = road_item['dm']
        if roadCode:
            gate_items = get_gate(gate='', roadCode=roadCode)
            if gate_items:
                # 存储楼栋号信息
                date = time_util.now_to_date("%Y-%m-%d")
                path = f'{date}_gate.csv'
                save(path, gate_items)


def batch_get_houses():
    gate_items = csv_util.read_csv2array("2021-03-29_gate.csv")
    for gate_item in gate_items:
        gateCode = gate_item['dm']
        houses = get_house(gateCode=gateCode)
        if houses:
            # 存储门牌号信息
            date = time_util.now_to_date("%Y-%m-%d")
            path = f'{date}_house.csv'
            save(path, gate_items)


def clear_repeat_data(path='2021-03-29_road.csv', des='road.csv', key='dm'):
    count = 0
    arr = []
    road_code_arr = []
    road_items = csv_util.read_csv2array(path)
    # 存储道路号信息
    for road_item in road_items:
        roadCode = road_item[key]
        if not roadCode in road_code_arr:
            count += 1
            print(f"【({count}).roadCode={roadCode}】")
            road_code_arr.append(roadCode)
            arr.append(road_item)
    save(des, arr, True)


def trim_to_road(road):
    road = road.replace('小市政', '')
    road = road.replace('小区门口', '')
    road = road.replace('路口', '')
    if '路口' in road:
        road = road.replace('口', '')
    search1 = re_util.find_texts_by_reg(r'(.*?)\(', road)
    if len(search1) > 0:
        # print(f"【trim_to_road().search1={search1}】")
        road = search1[0]
    search1 = re_util.find_texts_by_reg(r'(.*?)\（', road)
    if len(search1) > 0:
        # print(f"【trim_to_road().search1={search1}】")
        road = search1[0]
    road = re_util.removePunctuation(road)
    if road and len(road) > 1:
        searchs = re_util.find_texts_by_reg(r'(.*?)\d+', road)
        if len(searchs) > 0:
            if searchs[0] and len(searchs[0]) > 1:
                # print(f"【trim().searchs={searchs}】")
                return searchs[0]
            else:
                return None
        else:
            return road
    return None


def extra_roads(path='城市道路2017.csv', des='2017_road.csv'):
    arr = []
    road_items = csv_util.read_csv2array(path, encoding=ENCODING_GBK)
    for road_item in road_items:
        road = trim_to_road(road_item['路名'])
        start = trim_to_road(road_item['段起点'])
        end = trim_to_road(road_item['段止点'])
        if road:
            arr.append({'road_name': road})
        if start:
            arr.append({'road_name': start})
        if end:
            arr.append({'road_name': end})
    save(des, arr, True)


def batch():
    extra_roads(path='城市道路2017.csv', des='2017_road.csv')
    clear_repeat_data(path='2017_road.csv', des='2017_road_clear.csv', key='road_name')


def compare():
    arr = []
    road_items = csv_util.read_csv2array('dict_department_road_name.csv')
    map = [item['road_name'] for item in road_items]
    road_items = csv_util.read_csv2array('2017_road_clear.csv')
    for item in road_items:
        name_ = item['road_name']
        if not name_ in map:
            arr.append(item)
    save('2017_road_diff_lianjia.csv', arr, True)


def merge(a='2017_road_clear.csv', b='dict_department_road_name.csv', des='上海道路汇总.csv'):
    road_items = csv_util.read_csv2array(a)
    map = [item['road_name'] for item in road_items]
    road_items1 = csv_util.read_csv2array(b)
    for item in road_items1:
        road_name_ = item['road_name']
        name_ = trim_to_road(road_name_)
        if name_ and not name_ in map:
            road_items.append({'road_name': name_})
        else:
            print(f"【merge().name_={road_name_}】")
    save(des, road_items, True)


def test():
    roads = get_road('凯旋路')
    dm_ = roads[0]['dm']
    gates = get_gate(gate='1', roadCode=dm_)
    dm_ = gates[0]['dm']
    get_house(gateCode=dm_)


if __name__ == '__main__':
    # batch_getroads(path='2017_road_diff_lianjia.csv')
    date = time_util.now_to_date("%Y-%m-%d")
    clear_repeat_data(path='上海道路.csv', des=f'{date}上海道路汇总最终版.csv', key='road_name')
    # merge(a='高德.csv', b='上海道路汇总.csv', des='上海道路.csv')
