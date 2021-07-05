from PyQt5.QtWidgets import QMessageBox


def showMsg(parent, msg):
    QMessageBox.information(parent, '提示', msg,
                            QMessageBox.Ok,
                            QMessageBox.Ok)
