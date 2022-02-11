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

from house import Login
from proxy_util.UIQtThread import UIActionQtThread

"""
Basic skeleton of a mitmproxy addon.
Run as follows: mitmproxy -s anatomy.py
Run as follows: mitmdump -s anatomy.py
"""
keywords = ['appapi.5i5j.com']
# keywords = ['USBLogin','AppNavigatorIn51','main','List','apply','checkToken']


def filterUrl(urls):
    # return True
    for item in keywords:
        if item in urls:
            return True
    return False


def log(msg):
    print(msg)


class USBCounter:
    def __init__(self, thread: UIActionQtThread):
        self.num = 0
        self.did = None
        self.sid = None
        self._thread = thread

    def request(self, flow: HTTPFlow):
        self.num = self.num + 1
        url = flow.request.url
        if filterUrl(url):
            text = flow.request.text
            items = flow.request.headers.items()
            print(f"{flow.request.method}  {flow.request.url}")
            log("request text is  %s" % text)
            print(f"==request headers==========================")
            for item in items:
                log(f'"{item[0]}":"{item[1]}",')
            print(f"==request headers==========================")
            # log("host is  %s" % host)

            # log("We've seen %d flows" % self.num)

    def response(self, flow: HTTPFlow):
        data = {}
        url = flow.request.url
        if filterUrl(url):
            items = flow.response.headers.items()
            print(f"==response headers==========================")
            for item in items:
                log(f'"{item[0]}":"{item[1]}",')
            log(f"==response headers==========================")
            log(f"==response text==========================")
            log(f"{flow.response.text}")
            log(f"==response text==========================")
            for item in flow.response.cookies.items():
                log(f'"{item[0]}":"{item[1]}",')
            data['url'] = flow.request.url
            data['cookie'] = None
            data['cookie'] = flow.request.headers.get('Cookie')
            data['referer'] = flow.request.headers.get('Referer')
            data['location'] = flow.response.headers.get('Location')
            data['host'] = url
            data['method'] = flow.request.method
            try:
                data['param'] = json.loads(flow.request.text)
            except:
                data['param'] = flow.request.text
            dumps = json.dumps(data, indent=4, ensure_ascii=False)
            if (data['location']):
                print(f"==找到location==={data['location']}=====")
            # log("response  is  \n %s" % dumps)
            self.did = data['url']
            self.sid = data['referer']
            self.sessionId = data['cookie']
            if self.did or self.sid or self.sessionId:
                if self._thread:
                    self._thread.response(1, "获取到数据", [self.did, self.sid, self.sessionId])
            #     proxy_result_dialog.uppdate(self.did, self.sid, self.sessionId)
            # self.insert_item(
            #     {'account': self.did, 'password': self.sid, 'sessionId': self.sessionId})

    def insert_item(self, item):
        url = "http://preview.apiservices.zuber.im/agent/road/fgjsetting1"
        if not url:
            return
        try:
            item["type"] = "fgj"
            item["source"] = "wuju"
            item["key"] = "8D0903C6E3FFF3B17B3A4BF16F3041E9"
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
        counter = USBCounter(thread)
        addons = [
            counter
        ]
        self.master.addons.add(*addons)
        self.master.run()

    def start_mitweb(self, host=None, port: int = None, thread: UIActionQtThread = None):
        if thread:
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
    ServerManager().start('192.168.5.234', 8889)
    # ServerManager().start('192.168.5.234', 8889)
