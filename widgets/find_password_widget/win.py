import json
import re

from PyQt5 import QtWidgets

from settings import ServiceUri, ServicePort
from utils.check import check_email_valid, check_password_valid
from utils.qhttp import Http
from widgets.find_password_widget.find_password_widget import Ui_find_password_form


class FindPasswordWidget(QtWidgets.QDialog, Ui_find_password_form):
    def __init__(self, parent=None):
        super(FindPasswordWidget, self).__init__(parent)
        self.setupUi(self)

        self.find_email.textChanged.connect(self.check_email)
        self.find_email.setToolTip('用户名长度为6-20个字符，只能包含字母、数字、下划线')

        self.find_password.textChanged.connect(self.check_password)
        self.find_password.setToolTip('密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符')

        self.find_confirm_password.textChanged.connect(self.check_confirm_password)
        self.find_confirm_password.setToolTip('密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符')

        self.find_get_yzm_btn.clicked.connect(self.find_get_yzm_btn_clicked)
        self.find_confirm_btn.clicked.connect(self.find_confirm_btn_clicked)

        self.find_cancel_btn.clicked.connect(self.close)

        self.http = Http()

    def http_callback(self, reply):
        if reply.error():
            QtWidgets.QMessageBox.warning(self, '错误', '网络错误')
            return
        data = reply.readAll().data()
        data = json.loads(data)
        if data['type'] == 'error':
            QtWidgets.QMessageBox.warning(self, '提示信息', data['msg'])
        else:
            QtWidgets.QMessageBox.information(self, '提示信息', data['msg'])
        reply.deleteLater()

    def find_confirm_btn_clicked(self):
        # 检查邮箱是否合法
        email = self.find_email.text()
        if not check_email_valid(email):
            QtWidgets.QMessageBox.warning(self, '错误', '邮箱格式错误')
            return
        # 检查密码是否合法
        password = self.find_password.text()
        if not check_password_valid(password):
            QtWidgets.QMessageBox.warning(self, '错误', '密码格式错误')
            return
        # 检查两次密码是否一致
        confirm_password = self.find_confirm_password.text()
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, '错误', '两次密码不一致')
            return
        # 发送请求
        url = f'{ServiceUri}:{ServicePort}/user/find_password'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'email': email,
            'password': password,
            'yzm': self.find_yzm.text()
        }
        self.http.post(url, data, headers, self.http_callback)

    def find_get_yzm_btn_clicked(self):
        # 检查邮箱是否合法
        email = self.find_email.text()
        if not check_email_valid(email):
            QtWidgets.QMessageBox.warning(self, '错误', '邮箱格式错误')
            return
        # 发送验证码
        url = f'{ServiceUri}:{ServicePort}/user/find_password_yzm'
        data = {
            'email': email
        }
        headers = {
            'Content-Type': 'application/json'
        }
        self.http.post(url, data, headers, self.http_callback)

    def check_email(self, email):
        # 去除非法字符
        email = re.sub(r'[^a-zA-Z0-9_@.]', '', email)
        self.find_email.setText(email)

    def check_confirm_password(self, confirm_password):
        # 自动去除非法字符
        confirm_password = re.sub(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', '', confirm_password)
        self.find_confirm_password.setText(confirm_password)

    def check_password(self, password):
        # 自动去除非法字符
        password = re.sub(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', '', password)
        self.find_password.setText(password)
