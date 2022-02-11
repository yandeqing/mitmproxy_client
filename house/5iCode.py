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
from bs4 import BeautifulSoup

from utils import re_util, csv_util, FilePathUtil, time_util
from utils.re_util import find_texts_by_reg

header = {
    "Host": "sh.5i5j.com",
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:96.0)Gecko/20100101Firefox/96.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip,deflate,br",
    "Connection": "keep-alive",
    "Cookie": "SECKEY_ABVK=8ckL9a0OZW3pG7BxDommGOZBs8NDqNmmLBZh3j73t1Q%3D; BMAP_SECKEY=8ckL9a0OZW3pG7BxDommGK86f2QdszaPP7h7W6uD2nM-780bmpaE7dH7bc4G4BjUM01q-BKkiG6UyGDaMSlJNUXlAE8yZQwLUSHigdOzsLvxPuabtS0n0hOgocWfHS7uB_B_Es1vgwrNbOn8g0J-LzF06A1VdfNgj4fMAQBTaaz3urqPMdXSXE-0yv9-w2ar; morCon=open; HMF_CI=337a06324c5f1c7b7d2d40862aa1f5375483948144c3bdbf8ea0c9181aad6528a3; PHPSESSID=fj8c31qeu5sd1eb8ffelv1cna0; domain=sh; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1644220391; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1644227655; gr_user_id=fd385554-673a-4cbf-9839-e6226a470fbf; 8fcfcf2bd7c58141_gr_session_id_2be6f8f6-dc55-44af-8f36-9af35b962fa2=true; 8fcfcf2bd7c58141_gr_session_id=2be6f8f6-dc55-44af-8f36-9af35b962fa2; _ga=GA1.2.535774457.1644220392; _gid=GA1.2.1936913699.1644220392; zufang_BROWSES=45721281%2C45722849%2C45722208; HMY_JC=5927508d796ddc9a8d8b6007e3878863fb857fc27bfb013ab021a3d0244802481d,",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def format(content):
    return content.strip().replace(" ", "") \
        .replace("\n", "|").replace("\t", "") \
        .replace("||||", "|").replace("|||", "|") \
        .replace("||", "|")

date = time_util.now_to_date('%Y%m%d_%H')
path = FilePathUtil.get_full_dir("csv", f"hycode_{date}.csv")

last_href = ""
href_ = "https://sh.5i5j.com/zufang/v1/"
if __name__ == '__main__':
    session = requests.session()
    while last_href != href_:
        randint = random.randint(1, 5)
        print(f"【().randint={randint}】")
        time.sleep(randint)
        response = session.get(headers=header, url=href_)
        last_href = href_
        print(f'{response}')
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all(class_='listCon')
        if items is None:
            print(f"items is None")
            break
        print(f"size={len(items)}")
        excel_item={}
        for index, item in enumerate(items):
            links_items = item.find_all("a")
            links=[f"https://sh.5i5j.com{link['href']}" for link in links_items]
            excel_item['detail_href']=links[0]
            detail_response = session.get(headers=header, url=links[0])
            soup2 = BeautifulSoup(detail_response.text, 'html.parser')
            hy_code = soup2.find(class_='hy_code')
            if hy_code:
                excel_item['hy_code']=hy_code.text
            excel_item["intro"]=format(item.text)
            excel_items = []
            excel_items.append(excel_item)
            csv_util.append_csv(path, excel_items)
            print(f'{index}.{excel_item}')
        cPage = soup.find(class_='cPage')
        if cPage:
            href_ = f"https://sh.5i5j.com{cPage['href']}"


