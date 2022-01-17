import json
import sys
import threading

import requests
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QDialog, QDialogButtonBox, \
    QApplication

from proxy_util import confirm_dialog


class ProxyResultDialog(QDialog):
    def __init__(self, parent=None):
        super(ProxyResultDialog, self).__init__(parent)
        layout = QFormLayout()

        self.label = QLabel("上传接口:")
        self.le1 = QLineEdit()
        self.le1.setText("http://preview.apiservices.zuber.im/agent/road/fgjsetting")
        self.le1.setPlaceholderText("http://preview.apiservices.zuber.im/agent/road/fgjsetting")
        layout.addRow(self.label, self.le1)

        self.label = QLabel("\n抓取结果:")
        layout.addRow(self.label)
        self.label3 = QLineEdit("url")
        self.le3 = QLineEdit()
        layout.addRow(self.label3, self.le3)
        self.label4 = QLineEdit("referer")
        self.le4 = QLineEdit()
        layout.addRow(self.label4, self.le4)
        self.label5 = QLineEdit("cookie")
        self.le5 = QLineEdit()
        layout.addRow(self.label5, self.le5)

        self.cacelButton = QPushButton("关闭")
        self.uploadBtn = QPushButton("上传参数")
        self.cacelButton.clicked.connect(self.close)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.uploadBtn.clicked.connect(self.save)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.uploadBtn, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.cacelButton, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addRow(self.buttonBox)
        self.setLayout(layout)
        self.setWindowTitle("上传参数小工具")


    def save(self):
        did = self.le3.text()
        sid = self.le4.text()
        sessionId = self.le5.text()
        key1 = self.label3.text()
        key2 = self.label4.text()
        key3 = self.label5.text()
        res=self.insert_item({key1: did, key2: sid, key3: sessionId})
        if res['code']==0:
            confirm_dialog.showMsg(self,"上传成功！")
        else:
            confirm_dialog.showMsg(self,f"上传失败！{res}")


    def insert_item(self, item):
        url = self.le1.text()
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
            return res_json
        except Exception as e:
            print(e)
            return None



    def updateResult(self, did, sid, sessionId):
        self.le3.setText(did)
        self.le4.setText(sid)
        self.le5.setText(sessionId)


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

def uppdate(did, sid, sessionId):
    win = ProxyResultDialog()
    win.show()
    win.updateResult(did, sid, sessionId)
    win.setMinimumSize(560, 100)
    win.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ProxyResultDialog()
    arguments = app.arguments()
    if len(arguments) > 3:
        win.updateResult(arguments[1], arguments[2], arguments[3])
    win.show()
    win.setMinimumSize(560, 100)
    sys.exit(app.exec_())
