#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/3/31 13:58
'''
import json

import road_search

if __name__ == '__main__':
    arr = []
    count = 0
    key_arr = []
    with open('address.json', 'r', encoding='utf-8')as f:
        for line in f.readlines():
            loads = json.loads(line)
            loads_name_ = loads['name']
            type = loads['type']
            if not '路口名' in type and not '桥' in type \
                    and not '高速路入口' in type  \
                    and not '公司' in type and \
                    not '酒店' in type and not '住宿' in type:
                name_ = road_search.trim_to_road(loads_name_)
                if name_:
                    if not name_ in key_arr:
                        key_arr.append(name_)
                        item = {'road_name': name_}
                        arr.append(item)
                else:
                    count += 1
                    print(f'{count}.{loads_name_}')
                    print(f'type={type}')
        print(f'{len(arr)}')
        road_search.save('高德.csv', arr, force=True)
