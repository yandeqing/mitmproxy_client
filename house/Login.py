#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/12/16 10:27
'''

import webbrowser

def open_with360(path="C:\\Users\\Zuber\\AppData\\Roaming\\360se6\\Application\\360se.exe"):
    url = "http://183.194.243.146:7001/fangdi/system/AppNavigatorIn.nkin?appID=51&appPage=main&appEntry=183.194.244.244:8081"
    print(url)
    webbrowser.register('IE', None, webbrowser.BackgroundBrowser(path))
    webbrowser.get('IE').open(url, new=1, autoraise=True)
    # 或者
    # webbrowser.open_new_tab(url)


if __name__ == '__main__':
    open_with360()
    # http://183.194.243.146:7001/fangdi/system/USBLoginApp.jsp
    # open the defalut homepage
    # os.system(
    #     '"C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLogin.jsp')
    # os.system('"C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe" http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?keypwd=134cc70a')
