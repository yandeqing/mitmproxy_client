#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/1 17:18
'''
import road_search
from utils import csv_util


def count():
    words = ""
    keys = csv_util.read_csv2array("../2021-03-31上海道路汇总最终版.csv")
    for item in keys:
        name_ = item['road_name']
        words += name_
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    arr = []
    for i in range(len(items)):
        word, count = items[i]
        arr.append({'word': word, 'count': count})
        print("{0:<5}{1:<5}{2:<5}".format(i, word, count))
    road_search.save('road_word.csv', arr, force=True)


if __name__ == '__main__':
    count()
