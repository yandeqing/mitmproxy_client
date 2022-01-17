#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/12/16 10:27
'''
import json
import platform
import re
import sys
import time
import webbrowser
from ctypes import CDLL, WinDLL, windll
from urllib.parse import urlencode, quote

import requests

from house import Data_text
from utils import FilePathUtil
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

# 	POST /shhouse/system/USBServerCheck.jsp HTTP/1.1
# Accept	text/html, application/xhtml+xml, image/jxr, */*
# Referer	http://newsh.fangdi.com.cn:6001/shhouse/system/USBLoginCheck.jsp
# Accept-Language	zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3
# User-Agent	Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)
# Content-Type	application/x-www-form-urlencoded
# Accept-Encoding	gzip, deflate
# Content-Length	2638
# Host	newsh.fangdi.com.cn:6001
# Pragma	no-cache
headers = {
    "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
    "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
    "Accept-Encoding": "gzip, deflate",
    "Host": "newsh.fangdi.com.cn:6001",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://newsh.fangdi.com.cn:6001/shhouse/system/USBLoginCheck.jsp",
    # "Cookie": "AlteonP=AMfQUmTcHKwEyqkXbkEnZQ$$; JSESSIONID=48GGh9QPdGhFJGTXpm5Lk0PLxTmjJgcCZCkvJ0ZqTt9zKdzcJnrY!1901622873",
}


def USBLogin():
    url = "http://newsh.fangdi.com.cn:6001/shhouse/system/USBLogin.jsp"
    response=  start_request(url,None)
    cookie_ = response.headers['Set-Cookie']
    print(f"{cookie_}")
    return cookie_

def USBLoginCheck(cookie):
    url = "http://newsh.fangdi.com.cn:6001/shhouse/system/USBLoginCheck.jsp"
    response=  start_request(url,"pwd=14e797ae",cookie)
    cookie_ = response.headers['Set-Cookie']
    print(f"{cookie_}")
    return cookie_


def start_request(url, payload,cookie=None):
    print(f"=====url={url}=====")
    print(f"post {payload}")
    headers['Cookie']=cookie
    print(f"headers={json.dumps(headers, indent=4, ensure_ascii=False)}")
    response = requests.post(url, headers=headers, data=payload)
    print(f"==responses tatus_code= {response.status_code}==========================")
    print(f"==response text={response.text}==========================")
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    return response


def USBLoginApp(cookie):
    print(f"=====login2=====")
    url = "http://newsh.fangdi.com.cn:6001/shhouse/system/USBServerCheck.jsp"
    payload = 'sCert=MIIGQTCCBSmgAwIBAgIQQvM9ida5ZQFwmMM%2B85AsITANBgkqhkiG9w0BAQsFADAzMQswCQYDVQQGEwJDTjERMA8GA1UECgwIV' \
              'W5pVHJ1c3QxETAPBgNVBAMMCFNIRUNBIEcyMB4XDTE5MTEyODAyMTIwNFoXDTIxMTEyODE1NTk1OVowZjELMAkGA1UEBhMCQ04x' \
              'DzANBgNVBAgMBuS4iua1tzEPMA0GA1UEBwwG5LiK5rW3MSEwHwYJKoZIhvcNAQkBFhJudWxsQGZhbmdkaS5jb20uY24' \
              'xEjAQBgNVBAMMCeW8oOWbveeRnjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALUqVfo6lEdoKpwKh5LUA5Tg5esbidoS%2B' \
              '2bha6esKAbMgfOgms%2FNFrln6SJXWi3wMSmbAEkFTddesRVBUcG3ckwEkftyYfbxyf6ERp54PhrCwKYsabyA8D74f64meO3isATJ5A2ETfowzSQ6aK8pf%2FWFTmG' \
              '4onBtoNg4vtDfT1WEZ9CJYa%2BwypyHMT3%2BUKxj%2Ftm13YN8ZyyjB7LbPhJlOXmQvtN2aVwq5OkqzMpIrHCWQF40FLHp8e2Ct16njvSTNEhV9U2z%2Bt%2F' \
              '%2FbX6phJEnDKWsy%2Bb7cO3g17yspwo66S0bmqrgNzhJH0y02OGyuoQQ4BrkQfCE3b3vD%2B7ItLujC%2FcCAwEAAaOCAxwwggMYMB8GA1UdIwQYMBaAFFaI3u' \
              'MYQ4K3cqQm60SpYtCHxKwmMB0GA1UdDgQWBBRKs52cXsDy6O9IWpf5Nppwd%2FQ1QDALBgNVHQ8EBAMCBsAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGA' \
              'QUFBwMEMEEGA1UdIAQ6MDgwNgYIKoEcAcU4gRUwKjAoBggrBgEFBQcCARYcaHR0cDovL3d3dy5zaGVjYS5jb20vcG9saWN5LzAJBgNVHRMEAjAAMH0GCCsGAQU' \
              'FBwEBBHEwbzA4BggrBgEFBQcwAYYsaHR0cDovL29jc3AzLnNoZWNhLmNvbS9vY3NwL3NoZWNhL3NoZWNhLm9jc3AwMwYIKwYBBQUHMAKGJ2h0dHA6Ly9sZGFw' \
              'Mi5zaGVjYS5jb20vcm9vdC9zaGVjYWcyLmRlcjCB6gYDVR0fBIHiMIHfMDygOqA4hjZodHRwOi8vbGRhcDIuc2hlY2EuY29tL0NBMjAwMTEvUkExMjA1MDEwMC9DUkw1MjMxMi5jc' \
              'mwwgZ6ggZuggZiGgZVsZGFwOi8vbGRhcDIuc2hlY2EuY29tOjM4OS9jbj1DUkw1MjMxMi5jcmwsb3U9UkExMjA1MDEwMCxvdT1DQTIwMDExLG91PWNybCx' \
              'vPVVuaVRydXN0P2NlcnRpZmljYXRlUmV2b2NhdGlvbkxpc3Q%2FYmFzZT9vYmplY3RDbGFzcz1jUkxEaXN0cmlidXRpb25Qb2ludDCB7wYGKoEcAcU4BIHkMI' \
              'HhMEkGCCqBHAHFOIEQBD1sZGFwOi8vbGRhcDIuc2hlY2EuY29tL291PXNoZWNhIGNlcnRpZmljYXRlIGNoYWluLG89c2hlY2EuY29tMBEGCCqBHAH' \
              'FOIETBAU2NTc5OTAgBggqgRwBxTiBFAQUU0YzNDI2MDExOTc5MDMyNjMzM1gwEwYJKoEcAcU4gSoBBAZTSEZEWlkwDgYJKoEcAcU4gS' \
              'oCBAEyMA8GCSqBHAHFOIEqBAQCMjAwKQYJKoEcAcU4gSoFBBxTSEZEWlktMDItMzQyNjAxMTk3OTAzMjYzMzNYMA0GCSqGSIb3DQEBCwUAA' \
              '4IBAQDQMq90YfaHFYZi1Wxj%2BF%2Fgrx175IdWjp2MCLBIaJkYCA%2FcZaACzRObyWNOnkzHTQH5%2F%2F0QjNWvSvebif1wKUf9oh%2BsAtedbrQ' \
              'hm6il2GQdgr%2Fg17%2BMyPerWUYhXQM14hvmk1VESeXnBUrF13S%2FUfqz%2BnSE3Y%2FavWebsiBt7ETHmg8NvzP66Q5VDYjfhfAsODtaFMvfey0%2Bayf6pv' \
              'Fj1lh2m4F99AmUXIMk4FPkzjxNvO%2F6HYXHgX60%2BGydx%2Fs12RZhDo1hPHmXMdLZIBc1LXYmPCc46SkA%2FE%2Bg%2FaXPGlL%2Fg6CAPyq0Vzc93mw' \
              'TPwq5u5tAF9ve%2BDG0s5nRt1l%2Fd%2Bb%2F&sSign=amXpXglFLAE%2BHa8JHJdOuMsT4ObrlUvYS8PDkTsG46%2FZZdp2jRLPP4m38tJUZVJS07UxN' \
              'feYTxiW5J71y5DNMbe2D0ywB1XFGIB4RvRO8HQpi28jqojclJN%2BHdozVxnyEkjAoXrjiSCk340jGzljFTUdDWe6SaRYNTGGOtw4Tk8epjtF%2BjgFVh' \
              '3xZXdI2BIMUqGgOr7gMq7%2BML2mG0dNxatIYiziCmh%2FrmViMemY68%2B6yjlchAHskTQ4RN47H4wQZwt9otET0yyvcTaEiOwPIuJgEgJuXURQPWz%' \
              '2FOLp1ajv%2BL%2FcruWD5TcHfrtYwlIeytNNDlifI0dBqEtF5VVGWnA%3D%3D&sCredential=SHFDZY-02-34260119790326333X'
    response = start_request(url, payload,cookie)
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
    cookie = USBLogin()
    time.sleep(1)
    # cookie = trim_cookie(cookie)
    res = USBLoginCheck(cookie)
    time.sleep(1)
    res = USBLoginApp(cookie)


    # if res:
    #     cookie = trim_cookie(res)
    # time.sleep(1)
    # res = MiddAppList(cookie)
    # if res:
    #     cookie = trim_cookie(res)
    # res = AppNavigatorIn51(cookie)
    # split = cookie.split("; ")
    # split.reverse()
    # cookie = ("; ").join(split)
    # time.sleep(1)
    # res = AppNavigatorIn47(cookie)

    # sCredential: FWCXZX-47-913101203423709334
    # pwd:         134cc70a
    # http://183.194.243.146:7001/fangdi/system/USBLoginApp.jsp
    # open the defalut homepage
    # os.system(
    #     '"C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLogin.jsp')
    # os.system('"C:/Users/ZuberZuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?keypwd=134cc70a')

def getSign():
    path=FilePathUtil.get_full_dir("house","SafeEngine.dll")
    # path="C:/Windows/SysWOW64/SafeEngine.dll"
    # ----------以下四种加载DLL方式皆可—————————
    # SafeEngineCtl = WinDLL(path)
    # pDll = windll.LoadLibrary("./myTest.dll")
    # pDll = cdll.LoadLibrary("./myTest.dll")
    print(sys.platform)
    print(platform.architecture())
    SafeEngineCtl =  windll.LoadLibrary(path)
    # 调用动态链接库函数
    strSigned = SafeEngineCtl.SEH_SignData("157364", 3)
    # 打印返回结果
    print(f"【getSign().strSigned={strSigned}】")

def getAscii(item):
    return str(item)

if __name__ == '__main__':
    # getSign()
    # str="".join([getAscii(item) for item in Data_text.data_text[0:0x20D0]])
    # print(str)
    permitNo=quote('沪(2021)浦字不动产权第097886号'.encode('gb2312'))
    payload={}
    print(permitNo)
    cookie="JSESSIONID=C1vRhcMGFhVdYdn5Vq6GjscQ0TnRchqjlwBwvTMJT92nsL7WhBB4!-1895009612; trade.fangdi.com.cn.shhouse=trade.fangdi.com.cn.shhouse_rs1; trade.fangdi.com_6001_backup=trade.fangdi.com_6001_RS_backup; trade.fangdi.com.cn.SHFirstHouse=trade.fangdi.com.cn.SHFirstHouse_rs3"
    start_request("http://newsh.fangdi.com.cn:6001/shhouse/shhouse/common/HouseSelected.jsp?selectFlag=1",payload,cookie)
    start_request(f"http://newsh.fangdi.com.cn:6001/shhouse/shhouse/common/HouseSelected.jsp?selectFlag=1&houseID=&districtID=14&permitNo={permitNo}",payload,cookie)
    start_request("http://newsh.fangdi.com.cn:6001/shhouse/shhouse/common/HouseBuliding.jsp?buildingID=2502941319&regionID=14",payload,cookie)
    # permitNo=%BB%A6%282021%29%C6%D6%D7%D6%B2%BB%B6%AF%B2%FA%C8%A8%B5%DA097886%BA%C5