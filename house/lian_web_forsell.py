#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/12/16 10:27
'''
import json
import random
import time
import webbrowser

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

from utils import re_util, csv_util, FilePathUtil, time_util
from utils.re_util import find_texts_by_reg

header = {
    'Host': 'sh.lianjia.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.300',
    'Cookie': 'lianjia_ssid=9cfdc66f-c77f-4f79-968d-d21ffb56c180; lianjia_uuid=59ef7961-be5a-48c9-b3bb-43db4b3ffa72; select_city=310000'
}


def format_link(link):
    # splits = link.split(".jpg")
    # if len(splits) > 1:
    #     return f"{splits[0]}.jpg"
    # else:
    return link


def format(content):
    return content.strip().replace(" ", "") \
        .replace("\n", "|").replace("\t", "") \
        .replace("||||", "|").replace("|||", "|") \
        .replace("||", "|")


def get_soup(session, url):
    print(f"【url={url}】")
    response = session.get(headers=header, url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup





def start():
    date = time_util.now_to_date('%Y%m%d_%H')
    path = FilePathUtil.get_full_dir("csv", f"hycode_{date}.csv")
    pre_index = 0
    total_count = 0
    city = '上海'
    session = requests.session()
    soup = get_soup(session, "https://sh.lianjia.com/zufang/")
    # filter_content = soup.find('ul',{'data-target':'station'})
    filter_content = soup.find('ul', {'data-target': 'area'})
    filter_items = filter_content.find_all("a")
    links = [f"https://sh.lianjia.com{link['href']}" for link in filter_items]
    labels = [link.text for link in filter_items][1:]
    for i, item in enumerate(links[1:]):
        soup = get_soup(session, item)
        filter_contents = soup.find_all('ul', {'data-target': 'area'})
        sub_filters_content = filter_contents[1]
        sub_filter_items = sub_filters_content.find_all("a")
        sub_links = [f"https://sh.lianjia.com{link['href']}" for link in sub_filter_items]
        sub_labels = [link.text for link in sub_filter_items][1:]
        for j, subitem in enumerate(sub_links[1:]):
            soup = get_soup(session, subitem)
            item_count = soup.find(class_='content__title--hl')
            if item_count:
                total_count = int(item_count.text)
                if total_count == 0:
                    print(f"暂无数据")
                    break
            page_navigation = soup.find('div', {'data-el': 'page_navigation'})
            total_page = 1
            if page_navigation:
                total_page = page_navigation.attrs.get('data-totalpage')
                if total_page:
                    total_page = int(total_page)
            for page_index in range(1, total_page + 1):
                # randint = random.randint(1, 5)
                # print(f"【().randint={randint}】")
                # time.sleep(randint)
                href_ = f"{subitem}/pg{page_index}/#contentList"
                soup = get_soup(session, href_)
                items = soup.find_all(class_='content__list--item')
                if items is None:
                    print(f"items is None")
                    break
                excel_item = {'city': city, 'area': labels[i], 'business_district': sub_labels[j]}
                for index, item in enumerate(items):
                    house_code = item.attrs.get('data-house_code')
                    excel_item['house_code'] = house_code
                    links_items = item.find_all("a")
                    links = [f"https://sh.lianjia.com{link['href']}" for link in links_items]
                    soup2 = get_soup(session, links[0])
                    hy_code = soup2.find(class_='gov_title')
                    # piclist = soup2.find(class_='content__thumb--box')
                    piclist = soup2.find(class_='piclist')
                    if hy_code:
                        excel_item['hy_code'] = format(hy_code.text)
                    excel_item["intro"] = format(item.text)
                    excel_item['detail_href'] = links[0]
                    if piclist:
                        pic_links_items = piclist.find_all("img")
                        pic_links = [format_link(link['src']) for link in pic_links_items]
                        excel_item['pics'] = ";".join(pic_links)
                    else:
                        excel_item['pics'] = ""
                    excel_items = [excel_item]
                    csv_util.append_csv(path, excel_items)
                    pre_index = pre_index + 1
                    print(
                        f'{labels[i]}/{sub_labels[j]}（{page_index}/{total_page}）：{pre_index}.{excel_item["intro"]}')
                print(
                    f"page_index={page_index},total_page={total_page},page_size={len(items)},total_count={total_count}")
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}任务完成")

def job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))
    randint = random.randint(0, 60 * 20)
    formattime = time_util.change_to_formattime(randint)
    print(f'延迟{formattime}后执行')
    time.sleep(randint)
    start()


interval = 2

if __name__ == '__main__':
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"{t}启动任务")
    scheduler = BlockingScheduler()
    # 在每天9和21点的25分，运行一次 job 方法
    scheduler.add_job(job, 'cron', hour=f'8-23/{interval}', args=[f'8-23 每{interval}小时执行一次任务'])
    scheduler.start()
