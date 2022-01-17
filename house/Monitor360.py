#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/10 10:46
'''
import time
import webbrowser

from pykeyboard import PyKeyboard
from pymouse import PyMouse

from proxy_util import shell_util

if __name__ == '__main__':
    shell_util.exe_shell("taskkill /F /IM 360se.exe")
    webbrowser.register('IE', None, webbrowser.BackgroundBrowser("C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe"))
    webobject = webbrowser.get('IE')
    webobject.open("http://newsh.fangdi.com.cn:6001/shhouse/system/USBLogin.jsp")
    m = PyMouse()
    k = PyKeyboard()
    time.sleep(25)
    m.move(980, 530)
    time.sleep(1)
    m.click(980, 530)
    print(f"【m().position={m.position()}】")
    time.sleep(1)
    k.type_string("14e797ae")
    time.sleep(1)
    k.tap_key(k.enter_key)