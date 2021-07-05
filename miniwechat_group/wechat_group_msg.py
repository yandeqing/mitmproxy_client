#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/10 17:30
'''
import json
import random
import time

import requests
# {
#     "wx_msg_id": 20780973,
#     "content": "付佣给钱就租[社会社会]可短租\n\n①瑞冬小区女生合租￥1600\n②虹康三期朝北单间￥1900\n\n朋友圈有照片价格可谈\n随时看房☎️张183-2172-1232",
#     "create_time": 1618047061,
#     "lan_co_id": 25069,
#     "lan_co_name": "冯维（分散式）",
#     "lan_name": "冯**",
#     "lan_mobile": "15618935367",
#     "lan_co_mobile": "18317126073"
# }
from apscheduler.schedulers.blocking import BlockingScheduler

from utils import time_util, csv_util


def getUrl(page, city_id=1):
    url = f'https://m.baletu.com/sh/Houseapi/weixinHouseMsg?user_id=67129&search=&city_id={city_id}&p={page}' \
          '&from=31&preset_parameters=%7B%22%24latest_scene%22%3A%221178%22%2C%22%24url_path%22%3A%22pages%2Fwechathouse%2Fwechathouse%22%2C%22%24lib_version%22%3A%221.13.23%22%2C%22%24network_type%22%3A%22wifi%22%2C%22%24manufacturer%22%3A%22microsoft%22%2C%22%24model%22%3A%22microsoft%22%2C%22%24screen_width%22%3A414%2C%22%24screen_height%22%3A736%2C%22%24os%22%3A%22windows%22%2C%22%24os_version%22%3A%2210%22%2C%22_distinct_id%22%3A%22oM6K15IA4l7N5qh_gaXls6gBFbOQ%22%2C%22distinct_id%22%3A%22oM6K15IA4l7N5qh_gaXls6gBFbOQ%22%7D&public_parameters=%7B%22platformType%22%3A%22%E5%B0%8F%E7%A8%8B%E5%BA%8F%22%2C%22city_code%22%3A%22310100%22%2C%22is_login%22%3Afalse%2C%22device_id%22%3A%22oM6K15IA4l7N5qh_gaXls6gBFbOQ%22%2C%22blt_user_id%22%3A%220%22%2C%22project_name%22%3A%22%E5%87%BA%E4%B8%AA%E6%88%BF%E5%84%BF%E5%B0%8F%E7%A8%8B%E5%BA%8F%22%2C%22channel%22%3A%22%E5%B0%8F%E7%A8%8B%E5%BA%8F%22%2C%22openid%22%3A%22oM6K15IA4l7N5qh_gaXls6gBFbOQ%22%2C%22new_project_name%22%3A10%2C%22gps_city%22%3A%22%E4%B8%8A%E6%B5%B7%22%2C%22cookies_id%22%3A%220%22%7D&entrance=1'
    return url


def get_one_page(page, city_item=None):
    # print(f"【get_one_page().page={page}】")
    # print(f"【get_one_page().city_item={city_item}】")
    city_id = city_item['id']
    city_name = city_item['name']
    url = getUrl(page, city_id)
    # print(f"【get_one_page().url={url}】")
    get = requests.get(url)
    content = get.json()
    list_ = content['result']['list']
    last=len(list_)
    for index, item in enumerate(list_):
        create_time = time_util.timestamp_to_date(item['create_time'])
        item['create_time'] = create_time
        item['city'] = city_name
        # dumps = json.dumps(item, indent=2, ensure_ascii=False)
        # print(dumps)
        jsonstr = insert_item(item)
        if last==index:
            print(f"【uploadItems({index}).res={jsonstr}】")
    # date = time_util.now_to_date('%Y-%m-%d')
    # road_search.save(f'miniwechat_group_{date}.csv', list_)
    if list_ is None:
        return 0
    size = len(list_)
    return size


debug = False


def insert_item(item):
    if debug:
        return None
    try:
        res = requests.post("http://internal.zuker.im/moment/qzf", json=item)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        print(f"【insert_item().jsonstr={jsonstr}】")
        return jsonstr
    except Exception as e:
        print(e)
        return None


time_intervel = 60


def job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))
    arr = csv_util.read_csv2array('city_id.csv')
    sum = 0
    for item in arr:
        i = 0
        while True:
            i = i + 1
            length = get_one_page(i, item)
            sum = sum + length
            time.sleep(random.randint(1, 3))
            if length == 0:
                break
    print(f"【job.sum={sum}】")


if __name__ == '__main__':
    job('start')
    # t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print(f"{t}启动任务")
    # scheduler = BlockingScheduler()
    # # 在每天9和21点的25分，运行一次 job 方法
    # scheduler.add_job(job, 'cron', hour='8-23', minute='*/2', args=['8-23 每15分钟执行一次任务'])
    # scheduler.start()
