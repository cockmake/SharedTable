# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'u_s_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_u_s_dialog(object):
    def setupUi(self, u_s_dialog):
        u_s_dialog.setObjectName("u_s_dialog")
        u_s_dialog.resize(473, 583)
        font = QtGui.QFont()
        font.setPointSize(11)
        u_s_dialog.setFont(font)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(u_s_dialog)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(u_s_dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.year = QtWidgets.QDateEdit(u_s_dialog)
        self.year.setObjectName("year")
        self.horizontalLayout_2.addWidget(self.year)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(u_s_dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.search_key = QtWidgets.QLineEdit(u_s_dialog)
        self.search_key.setObjectName("search_key")
        self.verticalLayout.addWidget(self.search_key)
        self.yongchedanwei_select_all_btn = QtWidgets.QPushButton(u_s_dialog)
        self.yongchedanwei_select_all_btn.setObjectName("yongchedanwei_select_all_btn")
        self.verticalLayout.addWidget(self.yongchedanwei_select_all_btn)
        self.yongchedanwei_select_none_btn = QtWidgets.QPushButton(u_s_dialog)
        self.yongchedanwei_select_none_btn.setObjectName("yongchedanwei_select_none_btn")
        self.verticalLayout.addWidget(self.yongchedanwei_select_none_btn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.yongchedanweis = QtWidgets.QScrollArea(u_s_dialog)
        self.yongchedanweis.setWidgetResizable(True)
        self.yongchedanweis.setObjectName("yongchedanweis")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 341, 476))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.yongchedanweis.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.yongchedanweis)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel = QtWidgets.QPushButton(u_s_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.confirm = QtWidgets.QPushButton(u_s_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm.sizePolicy().hasHeightForWidth())
        self.confirm.setSizePolicy(sizePolicy)
        self.confirm.setObjectName("confirm")
        self.horizontalLayout.addWidget(self.confirm)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)

        self.retranslateUi(u_s_dialog)
        QtCore.QMetaObject.connectSlotsByName(u_s_dialog)

    def retranslateUi(self, u_s_dialog):
        _translate = QtCore.QCoreApplication.translate
        u_s_dialog.setWindowTitle(_translate("u_s_dialog", "客户账单统计"))
        self.label_2.setText(_translate("u_s_dialog", "年份"))
        self.year.setDisplayFormat(_translate("u_s_dialog", "yyyy"))
        self.label.setText(_translate("u_s_dialog", "用车单位"))
        self.search_key.setPlaceholderText(_translate("u_s_dialog", "搜索"))
        self.yongchedanwei_select_all_btn.setText(_translate("u_s_dialog", "全选"))
        self.yongchedanwei_select_none_btn.setText(_translate("u_s_dialog", "全不选"))
        self.cancel.setText(_translate("u_s_dialog", "取消"))
        self.confirm.setText(_translate("u_s_dialog", "确认"))
