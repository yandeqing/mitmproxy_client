#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/4/30 10:23
'''
import sys

import PyQt5
from PyQt5.QtCore import QThread, QCoreApplication


class UIActionQtThread(QThread):
    # result/code/msg
    signal = PyQt5.QtCore.pyqtSignal(dict)  # 定义信号对象,传递值为str类型，使用int，可以为int类型

    def __init__(self, callback=None):
        super(UIActionQtThread, self).__init__()
        self._callback = callback
        if self._callback:
            self.signal.connect(self._callback)

    def response(self, code, msg, result=None):
        self.signal.emit({'code': code, 'msg': msg, 'result': result})

    def bind(self, target, args):
        self._target = target
        self._args = args

    def stop_thread(self):
        try:
            if self.isRunning():
                self.quit()
                self.wait()
        except Exception as e:
            print(e)

    def run(self):
        try:
            if self._target:
                self._target(self._args)
        except Exception as e:
            print(e)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args



def printLog(msg):
    if msg:
        print(f"【printLog().msg={msg}】")


def printLog2(msg):
    if msg:
        print(f"【printLog2().msg={msg}】")


if __name__ == '__main__':
    app = QCoreApplication([])
    thread1 = UIActionQtThread()
    a = False
    thread1.bind(printLog, "你好")
    thread1.start()
    thread1.quit()
    thread1.wait()
    thread1.bind(printLog2, "你好")
    thread1.start()
    sys.exit(app.exec_())
