# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shared_table_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_shared_table_widget(object):
    def setupUi(self, shared_table_widget):
        shared_table_widget.setObjectName("shared_table_widget")
        shared_table_widget.resize(1121, 786)
        font = QtGui.QFont()
        font.setPointSize(11)
        shared_table_widget.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        shared_table_widget.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(shared_table_widget)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableWidget = MagicTable(self.centralwidget)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(17)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        self.horizontalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 45))
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.log_search_key_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_search_key_line_edit.sizePolicy().hasHeightForWidth())
        self.log_search_key_line_edit.setSizePolicy(sizePolicy)
        self.log_search_key_line_edit.setMinimumSize(QtCore.QSize(0, 45))
        self.log_search_key_line_edit.setFrame(True)
        self.log_search_key_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.log_search_key_line_edit.setDragEnabled(False)
        self.log_search_key_line_edit.setObjectName("log_search_key_line_edit")
        self.horizontalLayout_2.addWidget(self.log_search_key_line_edit)
        self.clear_log_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_log_btn.sizePolicy().hasHeightForWidth())
        self.clear_log_btn.setSizePolicy(sizePolicy)
        self.clear_log_btn.setMinimumSize(QtCore.QSize(0, 45))
        self.clear_log_btn.setObjectName("clear_log_btn")
        self.horizontalLayout_2.addWidget(self.clear_log_btn)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.logWidget = QtWidgets.QListWidget(self.centralwidget)
        self.logWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.logWidget.setAutoScrollMargin(16)
        self.logWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.logWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.logWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.logWidget.setObjectName("logWidget")
        self.verticalLayout_2.addWidget(self.logWidget)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.setStretch(0, 5)
        self.horizontalLayout_3.setStretch(1, 1)
        shared_table_widget.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(shared_table_widget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        shared_table_widget.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(shared_table_widget)
        self.statusbar.setObjectName("statusbar")
        shared_table_widget.setStatusBar(self.statusbar)
        self.add_one_row = QtWidgets.QAction(shared_table_widget)
        self.add_one_row.setObjectName("add_one_row")
        self.delete_selected_row = QtWidgets.QAction(shared_table_widget)
        self.delete_selected_row.setObjectName("delete_selected_row")
        self.user_logout = QtWidgets.QAction(shared_table_widget)
        self.user_logout.setObjectName("user_logout")
        self.main_table_search_action = QtWidgets.QAction(shared_table_widget)
        self.main_table_search_action.setObjectName("main_table_search_action")
        self.create_user_table_action = QtWidgets.QAction(shared_table_widget)
        self.create_user_table_action.setObjectName("create_user_table_action")
        self.create_wage_table_action = QtWidgets.QAction(shared_table_widget)
        self.create_wage_table_action.setObjectName("create_wage_table_action")
        self.u_s_action = QtWidgets.QAction(shared_table_widget)
        self.u_s_action.setObjectName("u_s_action")
        self.show_all_data_action = QtWidgets.QAction(shared_table_widget)
        self.show_all_data_action.setObjectName("show_all_data_action")
        self.export_main_table_action = QtWidgets.QAction(shared_table_widget)
        self.export_main_table_action.setObjectName("export_main_table_action")
        self.add_rows = QtWidgets.QAction(shared_table_widget)
        self.add_rows.setObjectName("add_rows")
        self.f_s_action = QtWidgets.QAction(shared_table_widget)
        self.f_s_action.setObjectName("f_s_action")
        self.menu.addSeparator()
        self.menu.addAction(self.add_rows)
        self.menu.addAction(self.add_one_row)
        self.menu.addAction(self.delete_selected_row)
        self.menu.addAction(self.export_main_table_action)
        self.menu_2.addAction(self.user_logout)
        self.menu_3.addAction(self.show_all_data_action)
        self.menu_3.addAction(self.main_table_search_action)
        self.menu_3.addAction(self.create_user_table_action)
        self.menu_3.addAction(self.create_wage_table_action)
        self.menu_3.addAction(self.u_s_action)
        self.menu_3.addAction(self.f_s_action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(shared_table_widget)
        QtCore.QMetaObject.connectSlotsByName(shared_table_widget)

    def retranslateUi(self, shared_table_widget):
        _translate = QtCore.QCoreApplication.translate
        shared_table_widget.setWindowTitle(_translate("shared_table_widget", "共享数据表"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("shared_table_widget", "序号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("shared_table_widget", "日期"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("shared_table_widget", "司机"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("shared_table_widget", "车号"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("shared_table_widget", "车型"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("shared_table_widget", "签单"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("shared_table_widget", "车属单位"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("shared_table_widget", "用车单位"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("shared_table_widget", "用车时间"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("shared_table_widget", "行程"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("shared_table_widget", "金额"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("shared_table_widget", "收"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("shared_table_widget", "票"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("shared_table_widget", "应付"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("shared_table_widget", "付"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("shared_table_widget", "结余"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("shared_table_widget", "备注"))
        self.label.setText(_translate("shared_table_widget", "操作历史"))
        self.log_search_key_line_edit.setPlaceholderText(_translate("shared_table_widget", "日志过滤"))
        self.clear_log_btn.setText(_translate("shared_table_widget", "清空"))
        self.logWidget.setSortingEnabled(False)
        self.menu.setTitle(_translate("shared_table_widget", "基础操作"))
        self.menu_2.setTitle(_translate("shared_table_widget", "用户"))
        self.menu_3.setTitle(_translate("shared_table_widget", "筛选"))
        self.add_one_row.setText(_translate("shared_table_widget", "添加一行"))
        self.delete_selected_row.setText(_translate("shared_table_widget", "删除所选"))
        self.user_logout.setText(_translate("shared_table_widget", "退出登录"))
        self.main_table_search_action.setText(_translate("shared_table_widget", "筛选详表"))
        self.create_user_table_action.setText(_translate("shared_table_widget", "查询账单"))
        self.create_wage_table_action.setText(_translate("shared_table_widget", "查询工资"))
        self.u_s_action.setText(_translate("shared_table_widget", "客户账单统计"))
        self.show_all_data_action.setText(_translate("shared_table_widget", "显示全部数据"))
        self.export_main_table_action.setText(_translate("shared_table_widget", "导出当前数据"))
        self.add_rows.setText(_translate("shared_table_widget", "批量添加"))
        self.f_s_action.setText(_translate("shared_table_widget", "财务统计"))
from MagicComponent import MagicTable
import assets_rc
