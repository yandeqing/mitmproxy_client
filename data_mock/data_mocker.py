#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/3/31 16:16
'''
import road_search
from utils import csv_util


def generate_road_code(min, max):
    pre = ['00号', '10号', '20号', '30号', '40号', '50号', '60号', '70号', '80号', '90号']
    length = 1
    arr = []
    for item in pre:
        arr.append({'keyword': item})

    for i in range(min, max + 1):
        arr.append({'keyword': str(i).zfill(length)[::-1] + "号"})
    return arr


def generate_roadcode(max):
    arr = []
    length = 1
    for i in range(1, max + 1):
        arr.append({'roadcode': str(i).zfill(length) + "号"})
    return arr


def search_text(text, path="road_codes.csv", limit=100):
    result = []
    road_items = csv_util.read_csv2array(path)
    for item in road_items:
        roadcode_ = item['roadcode']
        if text in roadcode_:
            result.append(item)
            if len(result) == limit:
                break
    return result


def test1():
    arr = generate_road_code(0, 99)
    road_search.save('road_code_keyword.txt', arr, force=True)
    print(arr)


def test2():
    arr = generate_roadcode(10008)
    road_search.save('road_codes.csv', arr, force=True)
    print(arr)


if __name__ == '__main__':
    test1()
    test2()
    arr = []
    keys = csv_util.read_csv2array("road_code_keyword.txt")
    for item in keys:
        roadcode_ = item['keyword']
        texts = search_text(roadcode_, path='road_codes.csv')
        arr.extend(texts)
        print(f"【search_text:({roadcode_})==>{len(texts)}条】")
    print(f"【累计={len(arr)}条】")

    arr_clear = []
    for item in arr:
        roadcode_ = item['roadcode']
        if not roadcode_ in arr_clear:
            arr_clear.append(roadcode_)
    print(f"【去重后{len(arr_clear)}条】")
