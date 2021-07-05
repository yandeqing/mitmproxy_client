#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/3/23 11:13
'''
import json
import os

from mitmproxy.http import HTTPFlow

from utils import FilePathUtil, time_util, csv_util

"""
Basic skeleton of a mitmproxy addon.
Run as follows: mitmproxy -s anatomy.py
Run as follows: mitmdump -s anatomy.py
"""
keywords = ['smartgate.ywtbsupappw.sh.gov.cn']


# keywords = ['homestay']


def filterUrl(host):
    # return True
    for item in keywords:
        if item in host:
            return True
    return False


def log(msg):
    print(msg)


class Counter:
    def __init__(self):
        self.num = 0
        self.did=None
        self.sid=None

    def request(self, flow: HTTPFlow):
        self.num = self.num + 1
        host = flow.request.host
        if filterUrl(host):
            text = flow.request
            items = flow.request.headers.items()
            log("headers  is  %s" % items)
            log("host is  %s" % host)
            log("text is  %s" % text)
            log("We've seen %d flows" % self.num)
            # for item in  flow.request.headers.items():
            #     log("header is  %s" % item)

    def response(self, flow: HTTPFlow):
        data = {}
        host = flow.request.host
        if filterUrl(host):
            data['url'] = flow.request.url
            data['x-tif-did'] = flow.request.headers.get('x-tif-did')
            data['x-tif-sid'] = flow.request.headers.get('x-tif-sid')
            data['host'] = host
            data['method'] = flow.request.method
            try:
                data['param'] = json.loads(flow.request.text)
            except:
                data['param'] = flow.request.text
            try:
                data['response'] = json.loads(flow.response.text)
            except:
                data['response'] = flow.response.text
            dumps = json.dumps(data, indent=4, ensure_ascii=False)
            log("response  is  \n %s" % dumps)
            keys = csv_util.get_head_from_arr([data])
            date = time_util.now_to_date('%Y%m%d_%H')
            path = FilePathUtil.get_full_dir("csv", f"{date}.csv")
            csv_util.create_csv(path, keys, force=False)
            csv_util.append_csv(path, [data])
            self.did = data['x-tif-did']
            self.sid = data['x-tif-sid']
            if  self.did:
                print(f"【response().did={self.did}】")
                print(f"【response().sid={self.sid}】")


counter = Counter()

addons = [
    counter
]


def start(host,port):
    shell=f'mitmdump.exe --listen-host {host} -p {port} -s anatomy.py'
    print(f"【exec_shell().shell={shell}】")
    os.system(shell)