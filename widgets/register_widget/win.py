import json
import re

from PyQt5 import QtWidgets

from settings import ServiceUri, ServicePort
from utils.check import check_email_valid, check_username_valid, check_phone_valid, check_password_valid
from utils.qhttp import Http
from widgets.register_widget.register_widget import Ui_register_form


class RegisterWidget(QtWidgets.QDialog, Ui_register_form):
    def __init__(self, parent=None):
        super(RegisterWidget, self).__init__(parent)
        self.setupUi(self)
        self.register_cancel_btn.clicked.connect(self.close)
        # username只允许输入字母、数字、下划线，长度为6-20个字符
        # 设置tooltip
        self.register_username.textChanged.connect(self.check_username)
        self.register_username.setToolTip('用户名长度为6-20个字符，只能包含字母、数字、下划线')
        # password只允许输入字母、数字、下划线、特殊字符，长度为8-16个字符
        # 设置tooltip
        self.register_password.textChanged.connect(self.check_password)
        self.register_password.setToolTip('密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符')
        # confirm_password只允许输入字母、数字、下划线、特殊字符，长度为8-16个字符
        # 设置tooltip
        self.register_confirm_password.textChanged.connect(self.check_confirm_password)
        self.register_confirm_password.setToolTip('密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符')
        # email只允许输入邮箱格式
        self.register_email.textChanged.connect(self.check_email)
        # yzm只允许输入数字
        self.register_yzm.textChanged.connect(self.check_yzm)
        # 手机号只允许输入数字
        self.register_phone.textChanged.connect(self.check_phone)

        self.register_confirm_btn.clicked.connect(self.register_confirm_btn_clicked)
        self.register_yzm_get_btn.clicked.connect(self.register_yzm_get_btn_clicked)

        self.http = Http()

    def check_phone(self, phone):
        # 去除非法字符
        phone = re.sub(r'[^0-9]', '', phone)
        self.register_phone.setText(phone)

    def check_yzm(self, yzm):
        # 去除非法字符
        yzm = re.sub(r'[^0-9]', '', yzm)
        self.register_yzm.setText(yzm)

    def check_email(self, email):
        # 去除非法字符
        email = re.sub(r'[^a-zA-Z0-9_@.]', '', email)
        self.register_email.setText(email)

    def check_confirm_password(self, confirm_password):
        # 自动去除非法字符
        confirm_password = re.sub(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', '', confirm_password)
        self.register_confirm_password.setText(confirm_password)

    def check_password(self, password):
        # 自动去除非法字符
        password = re.sub(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', '', password)
        self.register_password.setText(password)

    def check_username(self, username):
        # 自动去除非法字符
        username = re.sub(r'[^a-zA-Z0-9_]', '', username)
        self.register_username.setText(username)

    def register_yzm_get_callback(self, reply):
        json_byte = reply.readAll().data()  # Byte
        data = json.loads(json_byte)
        if data['type'] == 'error':
            QtWidgets.QMessageBox.warning(self, '提示信息', data['msg'])
        else:
            QtWidgets.QMessageBox.information(self, '提示信息', data['msg'])
        reply.deleteLater()

    def register_yzm_get_btn_clicked(self):
        email = self.register_email.text()
        if not check_email_valid(email):
            QtWidgets.QMessageBox.warning(self, '提示信息', "邮箱格式不正确")
            return
        # 发送请求
        url = f'{ServiceUri}:{ServicePort}/user/register_yzm'
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "email": email
        }
        self.http.post(url, data, headers, self.register_yzm_get_callback)

    def register_confirm_callback(self, reply):
        json_byte = reply.readAll().data()
        data = json.loads(json_byte)
        if data['type'] == 'error':
            QtWidgets.QMessageBox.warning(self, '错误', data['msg'])
        else:
            QtWidgets.QMessageBox.information(self, '提示信息', data['msg'])
        reply.deleteLater()

    def register_confirm_btn_clicked(self):
        # 判断用户名是否合法
        username = self.register_username.text()
        if not check_username_valid(username):
            QtWidgets.QMessageBox.warning(self, '错误', "用户名长度为6-20个字符，只能包含字母、数字、下划线")
            return
        # 判断密码是否合法
        password = self.register_password.text()
        if not check_password_valid(password):
            QtWidgets.QMessageBox.warning(self, '错误', "密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符")
            return
        # 判断两次密码是否一致
        confirm_password = self.register_confirm_password.text()
        if confirm_password != password:
            QtWidgets.QMessageBox.warning(self, '错误', "两次密码不一致")
            return
        # 判断邮箱是否合法
        email = self.register_email.text()
        if not check_email_valid(email):
            QtWidgets.QMessageBox.warning(self, '错误', "邮箱格式不正确")
            return
        # 判断手机号是否合法
        phone = self.register_phone.text()
        if not check_phone_valid(phone):
            QtWidgets.QMessageBox.warning(self, '错误', "手机号只允许输入数字且长度为11位")
            return
        name = self.register_name.text()
        yzm = self.register_yzm.text()

        is_admin = self.admin_radio_btn.isChecked()

        url = f'{ServiceUri}:{ServicePort}/user/register'
        data = {
            "username": username,
            "email": email,
            "password": password,
            "yzm": yzm,
            "name": name,
            "phone": phone,
            "operation_type": "管理员" if is_admin else "普通"
        }
        headers = {
            "Content-Type": "application/json"
        }
        self.http.post(url, data, headers, self.register_confirm_callback)
