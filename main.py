import asyncio
import sys

from PyQt5 import QtWidgets, QtGui
from asyncqt import QEventLoop

from widgets.login_widget.win import LoginWidget
from widgets.main_widget.win import MainWidget
from widgets.shared_table_widget.win import SharedTableWin

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 初始化界面
    # 添加事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # 设置全局字体大小为11
    font = QtGui.QFont()
    font.setPointSize(11)
    app.setFont(font)

    LoginWindow = LoginWidget()
    LoginWindow.show()

    SharedTableWindow = SharedTableWin()
    LoginWindow.login_success_signal.connect(SharedTableWindow.after_login)
    LoginWindow.not_login_signal.connect(SharedTableWindow.close)

    MainWindow = MainWidget()
    LoginWindow.not_login_signal.connect(MainWindow.show)
    LoginWindow.login_success_signal.connect(MainWindow.close)

    # with loop:
    #     loop.run_forever()

    sys.exit(app.exec_())
