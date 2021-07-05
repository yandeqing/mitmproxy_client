#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/19 15:48
'''

import os
import platform

proxy = "proxy.example.com"
port = 8080


def start_proxy(proxy, port):
    os.system('networksetup -setwebproxy Ethernet ' + proxy + ' ' + port)


def stop_proxy():
    os.system('networksetup -setwebproxystate Ethernet off')


proxy_host = "192.168.5.234"
proxy_port = "8889"

if __name__ == '__main__':
    print(str.lower(platform.system()))
    start_proxy(proxy_host, proxy_port)
