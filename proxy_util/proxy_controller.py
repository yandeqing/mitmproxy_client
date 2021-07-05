#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/19 15:48
'''
import ctypes
import winreg

#########################################################################
KEY_ProxyEnable = "ProxyEnable"
KEY_ProxyServer = "ProxyServer"
KEY_ProxyOverride = "ProxyOverride"
KEY_XPATH = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
#########################################################################

'''
设置代理
  enable: 0关闭，1开启
  proxyIp: 代理服务器ip及端口，如 "192.168.70.127:808"
  IgnoreIp:忽略代理的ip或网址，如 "172.*;192.*;"
'''


def SetProxy(enable, proxyIp, IgnoreIp):
    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_XPATH, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(hKey, KEY_ProxyEnable, 0, winreg.REG_DWORD, enable)
    winreg.SetValueEx(hKey, KEY_ProxyServer, 0, winreg.REG_SZ, proxyIp)
    winreg.SetValueEx(hKey, KEY_ProxyOverride, 0, winreg.REG_SZ, IgnoreIp)
    winreg.CloseKey(hKey)
    refresh()

# 获取当前代理状态
def GetProxyStatus():
    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_XPATH, 0, winreg.KEY_ALL_ACCESS)
    retVal = winreg.QueryValueEx(hKey, KEY_ProxyEnable)
    winreg.CloseKey(hKey)
    return retVal[0] == 1


def switch(proxy_host="192.168.5.234:8889"):
    if GetProxyStatus():
        stop_proxy()
        print("关闭代理")
    else:
        start_proxy(proxy_host)
        print("打开代理")


def start_proxy(proxy_host):
    print(f"打开代理{proxy_host}")
    SetProxy(1, proxy_host, "preview.apiservices.zuber.im")


def stop_proxy():
    SetProxy(0, "", "")
    print("关闭代理")


proxy_host = "192.168.5.234:8889"

def refresh():
    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39
    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)

if __name__ == '__main__':
    stop_proxy()
    # start_proxy(proxy_host)
