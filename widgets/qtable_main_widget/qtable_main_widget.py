# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtable_main_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_qtable_main_widget(object):
    def setupUi(self, qtable_main_widget):
        qtable_main_widget.setObjectName("qtable_main_widget")
        qtable_main_widget.resize(1100, 800)
        font = QtGui.QFont()
        font.setPointSize(11)
        qtable_main_widget.setFont(font)
        self.centralwidget = QtWidgets.QWidget(qtable_main_widget)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = MagicTable(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        qtable_main_widget.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(qtable_main_widget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        qtable_main_widget.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(qtable_main_widget)
        self.statusbar.setObjectName("statusbar")
        qtable_main_widget.setStatusBar(self.statusbar)
        self.export_current_data_action = QtWidgets.QAction(qtable_main_widget)
        self.export_current_data_action.setObjectName("export_current_data_action")
        self.menu.addAction(self.export_current_data_action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(qtable_main_widget)
        QtCore.QMetaObject.connectSlotsByName(qtable_main_widget)

    def retranslateUi(self, qtable_main_widget):
        _translate = QtCore.QCoreApplication.translate
        qtable_main_widget.setWindowTitle(_translate("qtable_main_widget", "数据展示"))
        self.menu.setTitle(_translate("qtable_main_widget", "导出"))
        self.export_current_data_action.setText(_translate("qtable_main_widget", "导出当前数据"))
from MagicComponent import MagicTable
