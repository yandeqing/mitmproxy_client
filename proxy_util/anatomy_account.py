#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/3/23 11:13
'''
import json

import requests

from mitmproxy.http import HTTPFlow
from mitmdump import DumpMaster, Options
from mitmproxy.tools import main, web

from proxy_util.UIQtThread import UIActionQtThread

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
    def __init__(self, thread: UIActionQtThread):
        self.num = 0
        self.did = None
        self.sid = None
        self._thread = thread

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
            self.sessionId = None
            try:
                data['param'] = json.loads(flow.request.text)
                self.sessionId = data['param'].get('sessionId')
            except:
                data['param'] = flow.request.text
            try:
                data['response'] = json.loads(flow.response.text)
            except:
                data['response'] = flow.response.text
            if self.sessionId is None:
                try:
                    self.sessionId = data['response'].get('data').get('sessionId')
                except:
                    pass
            dumps = json.dumps(data, indent=4, ensure_ascii=False)
            log("response  is  \n %s" % dumps)
            self.did = data['x-tif-did']
            self.sid = data['x-tif-sid']
            if self.did and self.sid and self.sessionId:
                if self._thread:
                    self._thread.response(1, "获取到数据", [self.did, self.sid, self.sessionId])
            #     proxy_result_dialog.uppdate(self.did, self.sid, self.sessionId)
            # self.insert_item(
            #     {'account': self.did, 'password': self.sid, 'sessionId': self.sessionId})

    def insert_item(self, item):
        url = "http://preview.apiservices.zuber.im/agent/road/ssbsetting"
        if not url:
            return
        try:
            res = requests.post(url, json=item)
            res_json = res.json()
            jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
            print(f"【insert_item().insert_item={item};res={jsonstr}】")
            return jsonstr
        except Exception as e:
            print(e)
            return None


class ServerManager:
    def __init__(self):
        super().__init__()
        self.master = None
        self._thread = None

    def start(self, host, port: int, thread: UIActionQtThread = None):
        opts = Options(listen_host=host, listen_port=port, scripts=None)
        self.master = DumpMaster(opts)
        self._thread = thread
        counter = Counter(thread)
        addons = [
            counter
        ]
        self.master.addons.add(*addons)
        self.master.run()

    def start_mitweb(self, host=None, port: int = None, thread: UIActionQtThread = None):
        thread.response(0, "web查看接口信息服务启动")
        args = [
            "--web-open-browser",
            "--listen-host",
            host,
            "--listen-port",
            str(port),
        ]
        # web.master.WebMaster(Options(listen_host=host, listen_port=port)).shutdown()
        main.mitmweb(args)


    def shutdown(self):
        self._thread.response(0, "shutdown", None)
        self.master.shutdown()


if __name__ == '__main__':
    # opts = Options(listen_host='0.0.0.0', listen_port=8888, scripts=__file__)
    # m = DumpMaster(opts)
    # m.run()
    ServerManager().start_mitweb('192.168.5.234', 8889)
    # ServerManager().start('192.168.5.234', 8889)
