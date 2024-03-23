import json
import re

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from settings import ServiceUri, ServicePort
from utils.qhttp import Http
from widgets.find_password_widget.win import FindPasswordWidget
from widgets.login_widget.login_widget import Ui_login_form
from widgets.register_widget.win import RegisterWidget


class LoginWidget(QtWidgets.QWidget, Ui_login_form):
    login_success_signal = pyqtSignal(str, str, str, str, dict)
    not_login_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.setupUi(self)

        self.register_btn.clicked.connect(self.register_btn_clicked)
        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.find_password_btn.clicked.connect(self.find_password_btn_clicked)
        # username只允许输入字母、数字、下划线，长度为6-20个字符
        # 设置tooltip
        self.login_username.textChanged.connect(self.check_username)
        self.login_username.setToolTip('用户名长度为6-20个字符，只能包含字母、数字、下划线')
        # password只允许输入字母、数字、下划线、特殊字符，长度为8-16个字符
        # 设置tooltip
        self.login_password.textChanged.connect(self.check_password)
        self.login_password.setToolTip('密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符')

        self.http = Http()

        self.not_login_btn.clicked.connect(self.not_login_btn_clicked)

        # 读取配置文件
        try:
            with open('.config.json', 'r') as f:
                data = json.load(f)
                username = data.get('username', '')
                password = data.get('password', '')
                self.login_username.setText(username)
                self.login_password.setText(password)
        except Exception as e:
            pass

    def not_login_btn_clicked(self):
        self.not_login_signal.emit()
        self.close()

    def find_password_btn_clicked(self):
        FindPasswordWidget(parent=self).exec_()

    def check_password(self, password):
        # 去除非法字符
        password = re.sub(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', '', password)
        self.login_password.setText(password)

    def check_username(self, username):
        # 去除非法字符
        username = re.sub(r'[^a-zA-Z0-9_]', '', username)
        self.login_username.setText(username)

    def login_btn_callback(self, reply):
        if reply.error():
            QtWidgets.QMessageBox.warning(self, '错误', '网络错误')
            return
        data = reply.readAll().data()
        data = json.loads(data)
        if data['type'] == 'error':
            QtWidgets.QMessageBox.warning(self, '提示信息', data['msg'])
        else:
            # 登录成功
            self.login_success_signal.emit(data['username'], data['name'],
                                           data['operation_type'], data['access_token'],
                                           data['privilege'])
            self.close()
        reply.deleteLater()

    def login_btn_clicked(self):
        username = self.login_username.text()
        password = self.login_password.text()
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, '错误', '用户名或密码不能为空')
            return

        url = f'{ServiceUri}:{ServicePort}/user/login'
        data = {
            'username': username,
            'password': password,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        if self.store_password_check_box.isChecked():
            with open('.config.json', 'w') as f:
                f.write(json.dumps({'username': username, 'password': password}))
        else:
            with open('.config.json', 'w') as f:
                f.write(json.dumps({'username': '', 'password': ''}))

        self.http.post(url, data, headers, self.login_btn_callback)

    def register_btn_clicked(self):
        register_widget = RegisterWidget(parent=self)
        register_widget.exec_()
