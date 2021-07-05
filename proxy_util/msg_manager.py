# coding:utf-8
import time
from threading import Thread

# 继承QThread
from PyQt5.QtCore import pyqtSignal, QThread


class Runthread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型

    def __init__(self, fuc_code=None):
        super(Runthread, self).__init__()
        #  通过类成员对象定义信号对象
        self.fuc_code = fuc_code

    def set_data(self, data):
        self.data = data

    def stop(self):
        self.exit(-1)

    def run(self):
        self.signals.emit("任务已完成")
