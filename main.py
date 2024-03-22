import sys

from PyQt5 import QtWidgets, QtGui

from widgets.login_widget.win import LoginWidget
from widgets.main_widget.win import MainWidget
from widgets.shared_table_widget.win import SharedTableWin

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 初始化界面
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

    sys.exit(app.exec_())  # 显示主窗口
