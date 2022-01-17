#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/15 17:19
'''
# a.py
import execjs


def getV():
    with open("aes.min.js", 'r', encoding='UTF-8') as fp:
        ajs = fp.read()
    loader = execjs.compile(ajs)
    r = loader.call('v')
    return r


if __name__ == "__main__":
    print(getV())
