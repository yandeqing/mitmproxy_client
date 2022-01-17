#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/12/16 10:27
'''
import json
import time
import webbrowser

import requests

from utils.re_util import find_texts_by_reg


def open_appnavigatorin(path):
    url = "http://183.194.243.146:7001/fangdi/system/AppNavigatorIn.nkin?appEntry=183.194.243.145:7001/rent/api/relogin&appPage=login.html&appID=47"
    # url = "http://183.194.243.146:7001/fangdi/system/AppNavigatorIn.nkin?appID=51&appPage=main&appEntry=183.194.244.244:8081"
    open(path, url=url)


webobject = None


def open(path=None, url=None):
    global webobject
    if webobject is None:
        webbrowser.register('IE', None, webbrowser.BackgroundBrowser(path))
        webobject = webbrowser.get('IE')
    webobject.open_new_tab(url)
    # 或者
    # webbrowser.open_new_tab(url)




def USBLoginCheck():
    print(f"=====login1=====")
    url = "http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?pwd=134cc70a"
    print(f"=====url={url}=====")
    payload = {}
    headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "183.194.243.146:7001",
        "Proxy-Connection": "Keep-Alive",
        # "Cookie": "AlteonP=AMfQUmTcHKwEyqkXbkEnZQ$$; JSESSIONID=48GGh9QPdGhFJGTXpm5Lk0PLxTmjJgcCZCkvJ0ZqTt9zKdzcJnrY!1901622873",
    }
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    response = requests.get(url, headers=headers, data=payload)
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    cookie_ = response.headers['Set-Cookie']
    print(f"{cookie_}")
    return cookie_


def USBLoginApp(cookie):
    print(f"=====login2=====")
    url = "http://183.194.243.146:7001/fangdi/system/USBLoginApp.jsp"
    print(f"=====url={url}=====")
    payload = 'sCredential=FWCXZX-47-913101203423709334&pwd=134cc70a'
    headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Referer": "http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?pwd=134cc70a",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "53",
        "Host": "183.194.243.146:7001",
        "Proxy-Connection": "Keep-Alive",
        "Pragma": "no-cache",
        "Cookie": cookie,
    }
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    print(f"post {payload}")
    response = requests.post(url, headers=headers, data=payload)
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    cookie_ = response.headers.get('Set-Cookie')
    print(f"{cookie_}")
    return cookie_


def AppNavigatorIn51(cookie):
    print(f"=====login3=====")
    url = "http://183.194.243.146:7001/fangdi/system/AppNavigatorIn.nkin?appID=51&appPage=main&appEntry=183.194.244.244:8081"
    print(f"=====url={url}=====")
    payload = {}
    headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "183.194.243.146:7001",
        "Proxy-Connection": "Keep-Alive",
        "Cookie": cookie
    }
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    response = requests.get(url, headers=headers, data=payload, allow_redirects=False)
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    print(f"content========={response.text}=====")
    cookie = response.headers.get('Set-Cookie')
    print(f"得到Cookie:{cookie}")
    return cookie


import http.cookiejar as HC


def AppNavigatorIn47(cookie):
    print(f"=====login4=====")
    url = "http://183.194.243.146:7001/fangdi/system/AppNavigatorIn.nkin?appEntry=183.194.243.145:7001/rent/api/relogin&appPage=login.html&appID=47"
    payload = {}
    headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Referer": "http://183.194.243.146:7001/fangdi/system/MiddAppList.jsp",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "183.194.243.146:7001",
        "Proxy-Connection": "Keep-Alive",
        "Connection": "Keep-Alive",
        "Cookie": cookie
    }
    print(f"=====url={url}=====")
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    session = requests.session()
    # session.cookies = HC.LWPCookieJar(filename='cookies')
    #  如果存在cookies文件，则加载，如果不存在则提示
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print('未找到cookies文件')
    response = session.get(url, headers=headers, data=payload, allow_redirects=False)
    # session.cookies.save()
    print_response(response)
    localtion = response.headers.get('Location')
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Connection': 'keep-alive'
    }
    # session.cookies.load(ignore_discard=True)
    response = session.get(localtion, headers=headers, data=payload, allow_redirects=False)
    print_response(response)
    localtion = response.headers.get('Location')
    response = session.get(localtion, headers=headers, allow_redirects=False)
    print_response(response)
    localtion = response.headers.get('Location')
    response = session.get(localtion, headers=headers, allow_redirects=False)
    print_response(response)

def print_response(response):
    print(f"url========={response.url}")
    print(f"status_code={response.status_code}")
    response.encoding = "utf-8"
    print(f"cookies======{response.cookies}=====")
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    print(f"response content========={response.text}")


def MiddAppList(cookies):
    print(f"=====getList=====")
    url = "http://183.194.243.146:7001/fangdi/system/MiddAppList.jsp"
    payload = {}
    headers = {
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "183.194.243.146:7001",
        "Proxy-Connection": "Keep-Alive",
        "Cookie": cookies
    }
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    response = requests.request("GET", url, headers=headers, data=payload)
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    # print(f"content========={response.text}=====")
    cookie_ = response.headers.get('Set-Cookie')
    return cookie_


def trim_cookie(cookie):
    reg = find_texts_by_reg(r'(JSESSIONID=.+?|AlteonP=.+?)(?=;)', cookie)
    search = "; ".join(reg)
    print(f"cookie={search}")
    return search


def login():
    cookie = USBLoginCheck()
    time.sleep(1)
    cookie = trim_cookie(cookie)
    res = USBLoginApp(cookie)
    if res:
        cookie = trim_cookie(res)
    time.sleep(1)
    res = MiddAppList(cookie)
    if res:
        cookie = trim_cookie(res)
    # res = AppNavigatorIn51(cookie)
    split = cookie.split("; ")
    split.reverse()
    cookie = ("; ").join(split)
    time.sleep(1)
    res = AppNavigatorIn47(cookie)

    # sCredential: FWCXZX-47-913101203423709334
    # pwd:         134cc70a
    # http://183.194.243.146:7001/fangdi/system/USBLoginApp.jsp
    # open the defalut homepage
    # os.system(
    #     '"C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLogin.jsp')
    # os.system('"C:/Users/ZuberZuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?keypwd=134cc70a')


if __name__ == '__main__':
    login()
