#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2022/1/15 11:02
'''
import time

from bluetooth import *


def getDevices():
    nearby_devices = discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    for item in nearby_devices:
        print(item)
    return nearby_devices


def connect(address, port):
    # Create the client socket
    client_socket = BluetoothSocket(RFCOMM)
    client_socket.connect((address, port))
    # client_socket.send("Hello World")
    print("Finished")
    # 进程一结束意味着连接断开，这里为了不断开用一个while循环来占用CPU
    # while True:
    #     time.sleep(0.001)
    client_socket.close()


if __name__ == '__main__':
    print("performing inquiry...")
    arr=getDevices()
    os.system("cmd")
    # getDevices()
    # connect("70:F0:87:0D:63:A2", 53)
