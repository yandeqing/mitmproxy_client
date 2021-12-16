import asyncio
import json
import sys
import threading

import requests
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox, \
    QApplication
from qtpy import QtWidgets

from house import Login
from proxy_util import anatomy_usblogin, proxy_controller, shell_util, \
    confirm_dialog
from proxy_util.UIQtThread import UIActionQtThread
from proxy_util.anatomy_usblogin import ServerManager
from proxy_util.proxy_uploader import ProxyResultDialog
from utils import time_util


class ProxySettingDialog(QDialog):
    def __init__(self, parent=None):
        super(ProxySettingDialog, self).__init__(parent)
        self.autoUpload = False
        self.win = None
        self.manager = None
        self.event = threading.Event()
        self.thread = UIActionQtThread(self.msg_callback)
        layout = QFormLayout()
        self.label = QLabel("IP,端口配置:")
        layout.addRow(self.label)
        self.label = QLabel("host")
        self.le1 = QLineEdit()
        ip = get_host_ip()
        self.le1.setText(ip)
        layout.addRow(self.label, self.le1)

        self.label = QLabel("port")
        self.le2 = QLineEdit()
        self.le2.setText("8889")
        layout.addRow(self.label, self.le2)

        self.label = QLabel("小程序快捷方式")
        self.le3 = QLineEdit()
        self.le3.setText(
            '"C:\Program Files (x86)\Tencent\WeChat\WechatAppLauncher.exe" -launch_appid=wxc5059c3803665d9c')
        layout.addRow(self.label, self.le3)

        self.label = QLabel("浏览器快捷方式")
        self.le4 = QLineEdit()
        self.le4.setText(
            "C:/Users/Zuber/AppData/Roaming/360se6/Application/360se.exe")
        layout.addRow(self.label, self.le4)

        self.label = QLabel("启动链接")
        self.le5 = QLineEdit()
        self.le5.setText(
            'http://183.194.243.146:7001/fangdi/system/USBLoginCheck.jsp?pwd=134cc70a')
        layout.addRow(self.label, self.le5)

        self.setProxyButton = QPushButton("设置代理")
        self.certButton = QPushButton("配置证书（已匹配请忽略）")
        self.saveButton = QPushButton("启动代理服务器")
        self.cacelProxyButton = QPushButton("取消代理")
        self.startWeb = QPushButton("启动浏览器")
        self.enterWeb = QPushButton("直接进入系统")
        self.stopWeb = QPushButton("关闭浏览器")
        self.miniBtn = QPushButton("启动小程序")
        self.miniStopBtn = QPushButton("关闭小程序")
        self.webBtn = QPushButton("可视化调试模式")
        self.autoBtn = QPushButton("启动自动化")
        self.autoStopBtn = QPushButton("关闭自动化")
        self.certButton.clicked.connect(
            self.clickCertButton)
        self.webBtn.clicked.connect(self.thread_startweb)
        self.miniBtn.clicked.connect(self.startMini)
        self.miniStopBtn.clicked.connect(self.stopMini)
        self.startWeb.clicked.connect(self.threadStartApp)
        self.enterWeb.clicked.connect(self.threadEnterApp)
        self.stopWeb.clicked.connect(self.stopApp)
        self.autoBtn.clicked.connect(self.threadAutoStart)
        self.autoStopBtn.clicked.connect(self.autoStop)
        self.saveButton.clicked.connect(self.thread_save)
        self.setProxyButton.clicked.connect(self.set_proxy)
        self.cacelProxyButton.clicked.connect(self.cancel_proxy)

        self.buttonBox = QDialogButtonBox()
        self.label = QLabel("代理配置")
        self.buttonBox.addButton(self.certButton, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.cacelProxyButton, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.webBtn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addRow(self.label, self.buttonBox)

        self.buttonBox = QDialogButtonBox()
        self.label = QLabel("启动流程")
        self.buttonBox.addButton(self.setProxyButton, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.saveButton, QDialogButtonBox.ButtonRole.AcceptRole)
        layout.addRow(self.label, self.buttonBox)

        self.label = QLabel("半自动化")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.startWeb, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.enterWeb, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.miniBtn, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(self.stopWeb, QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(self.miniStopBtn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addRow(self.label, self.buttonBox)

        self.label = QLabel("全自动化")
        self.buttonBox2 = QDialogButtonBox()
        self.buttonBox2.addButton(self.autoBtn, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox2.addButton(self.autoStopBtn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addRow(self.buttonBox2)
        self.buttonBox2 = QDialogButtonBox()
        self.buttonBox2.addButton(self.autoBtn, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox2.addButton(self.autoStopBtn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addRow(self.label, self.buttonBox2)

        self.setLayout(layout)
        self.setWindowTitle("代理设置小工具")

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "提示", "确定要退出吗?\n退出建议取消代理设置，否则将无法上网",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def thread_save(self):
        loop = asyncio.get_event_loop()
        self.thread_it(self.save, loop)

    def thread_startweb(self):
        loop = asyncio.get_event_loop()
        self.thread_it(self.start_web, loop)

    def clickCertButton(self):
        import webbrowser
        webbrowser.open("http://mitm.it/cert/p12")

    def set_proxy(self):
        host = self.le1.text()
        port = self.le2.text()
        proxy_controller.start_proxy(host + ":" + port)
        self.thread.response(0, '代理设置成功')

    def cancel_proxy(self):
        proxy_controller.stop_proxy()
        self.thread.response(0, '取消成功')

    def startMini(self):
        shell_cmd = self.le3.text()
        shell_util.exe_shell(shell_cmd)

    def stopMini(self):
        shell_util.exe_shell("taskkill /F /IM WeChatApp.exe")

    def threadStartApp(self):
        t = threading.Thread(target=self.startApp)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def startApp(self):
        shell_cmd = self.le4.text() + " " + self.le5.text()
        shell_util.exe_shell(shell_cmd)

    def threadEnterApp(self):
        t = threading.Thread(target=self.enterApp)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def enterApp(self):
        path = self.le4.text()
        Login.open_with360(path=path)

    def stopApp(self):
        shell_util.exe_shell("taskkill /F /IM 360se.exe")

    def threadAutoStart(self):
        self.set_proxy()
        self.event.wait(2)
        self.thread_save()
        t = threading.Thread(target=self.autoStart)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def autoStart(self):
        self.autoUpload = True
        while self.autoUpload:
            timecout = 10
            step = 1
            while timecout > 0:
                print(f"【autoStart(){timecout}s后检测是否需要自动获取上传】")
                timecout -= step
                self.event.wait(step)
                if not self.autoUpload:
                    break

            sys.stdout.flush()
            # os.system('cls')
            # 检测是否需要自动获取上传
            upload = self.need_upload()
            if upload:
                timeStr = time_util.now_to_date()
                print(f"【{timeStr}启动程序】")
                self.startApp()

    def autoStop(self):
        self.autoUpload = False
        self.stopApp()
        if self.manager:
            self.manager.shutdown()
            self.thread.stop_thread()

    def save(self, loop):
        host = self.le1.text()
        port = int(self.le2.text())
        if loop:
            asyncio.set_event_loop(loop)
        self.thread.response(0, "端口监听程序启动成功!")
        self.manager = ServerManager()
        self.manager.start(host, port, self.thread)

    def start_web(self, loop):
        host = self.le1.text()
        port = int(self.le2.text())
        if loop:
            asyncio.set_event_loop(loop)
        self.manager = ServerManager()
        self.manager.start_mitweb(host, port, self.thread)

    def showDialog(self, did, sid, sessionId):
        if self.win is None or not self.win.isVisible():
            self.win = ProxyResultDialog()
            self.win.show()
            self.win.updateResult(did, sid, sessionId)
            self.win.setMinimumSize(560, 100)
            # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
            # self.win.setWindowModality(QtCore.Qt.ApplicationModal)
            # self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
            self.win.exec_()
        else:
            self.win.updateResult(did, sid, sessionId)

    def msg_callback(self, *msg):
        res = msg[0]
        print(f"【msg_callback().res={res}】")
        if 1 == res['code']:
            args = res['result']
            if self.autoUpload:
                url = args[0]
                if "MiddAppList" in url:
                    self.enterApp()
                cookie = args[2]
                if cookie and cookie.startswith("JSESSIONID="):
                    print(f"【msg_callback().msg_callback=自动上传{args}")
                    res = self.insert_item(
                        {"url": url, "referer": args[1], "cookie": args[2]})
                    if res:
                        self.stopApp()
            else:
                self.showDialog(args[0], args[1], args[2])

        else:
            hint = res.get('msg')
            confirm_dialog.showMsg(self, hint)

    def insert_item(self, item):
        url = "http://preview.apiservices.zuber.im/agent/road/fgjsetting"
        # url = None
        try:
            res = requests.post(url, json=item)
            res_json = res.json()
            jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
            print(f"【insert_item().insert_item={item};res={jsonstr}】")
            return jsonstr
        except Exception as e:
            print(e)
            return None

    def need_upload(self):
        # if  True: return True
        url = "http://preview.apiservices.zuber.im/agent/road/fgjsetting"
        try:
            print(f"【检测是否需要更新.url={url}】")
            res = requests.get(url)
            res_json = res.json()
            print(f"【检测是否需要更新.response={res_json}】")
            return res_json.get('result')
        except Exception as e:
            print(e)
            return False

    def thread_it(self, func, args):
        self.thread.bind(func, args)
        self.thread.start()


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        import socket
        session = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        session.connect(('8.8.8.8', 80))
        ip = session.getsockname()[0]
    finally:
        session.close()
    return ip


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ProxySettingDialog()
    arguments = app.arguments()
    print(f"【().arguments={arguments}】")
    win.show()
    win.setMinimumSize(720, 100)
    sys.exit(app.exec_())
