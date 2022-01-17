#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/7/6 13:03
'''
import qrcode

if __name__ == '__main__':
    img = qrcode.make('https://resources.zuber.im/app/android202107061327-zuber-v1.7.2-137-20210706-d0dbdaf_v172_jiagu_sign.apk')
    # img.save("qr.png")
    img.show("qr.png")
