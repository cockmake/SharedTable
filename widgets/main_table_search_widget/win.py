from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from widgets.main_table_search_widget.main_table_search_widget import Ui_main_table_search_widget


class MainTableSearchWidget(QtWidgets.QDialog, Ui_main_table_search_widget):
    # 信号
    search_args_signal = pyqtSignal(dict)

    def __init__(self, yongchedanweis, cheshudanweis, drivers, fus, shous, parent=None):
        super(MainTableSearchWidget, self).__init__(parent=parent)
        self.setupUi(self)

        # 设置截止日期为今天
        self.date_end.setDate(QtCore.QDate.currentDate())
        self.search_btn_exec.setFocus()
        self.search_btn_exec.clicked.connect(self.search_btn_execute_clicked)
        self.cancel_btn.clicked.connect(self.close)
        self.yongchedanwei_search_key.textChanged.connect(self.yongchedanwei_search_key_changed)
        self.cheshudanwei_search_key.textChanged.connect(self.cheshudanwei_search_key_changed)
        self.driver_search_key.textChanged.connect(self.driver_search_key_changed)
        self.yongchedanwei_checkbox_list = []
        self.cheshudanwei_checkbox_list = []
        self.drivers_checkbox_list = []
        self.init_scroll_area(self.yongchedanweis_scroll_area, yongchedanweis, self.yongchedanwei_checkbox_list)
        self.init_scroll_area(self.cheshudanweis_scroll_area, cheshudanweis, self.cheshudanwei_checkbox_list)
        self.init_scroll_area(self.drivers_scroll_area, drivers, self.drivers_checkbox_list)

        fu_layout = QtWidgets.QVBoxLayout()
        fu_layout.setAlignment(Qt.AlignTop)
        self.fu_groupbox.setLayout(fu_layout)
        self.fu_checkbox_list = []
        for fu in fus:
            checkbox = QtWidgets.QCheckBox(fu)
            fu_layout.addWidget(checkbox)
            self.fu_checkbox_list.append(checkbox)

        shou_layout = QtWidgets.QVBoxLayout()
        shou_layout.setAlignment(Qt.AlignTop)
        self.shou_groupbox.setLayout(shou_layout)
        self.shou_checkbox_list = []
        for shou in shous:
            checkbox = QtWidgets.QCheckBox(shou)
            shou_layout.addWidget(checkbox)
            self.shou_checkbox_list.append(checkbox)

        self.yongchedanwei_select_all_btn.clicked.connect(self.yongchedanwei_select_all)
        self.yongchedanwei_select_none_btn.clicked.connect(self.yongchedanwei_select_none)
        self.cheshudanwei_select_all_btn.clicked.connect(self.cheshudanwei_select_all)
        self.cheshudanwei_select_none_btn.clicked.connect(self.cheshudanwei_select_none)
        self.driver_select_all_btn.clicked.connect(self.driver_select_all)
        self.driver_select_none_btn.clicked.connect(self.driver_select_none)

    def yongchedanwei_select_all(self):
        for checkbox in self.yongchedanwei_checkbox_list:
            if checkbox.isVisible():
                checkbox.setChecked(True)

    def yongchedanwei_select_none(self):
        for checkbox in self.yongchedanwei_checkbox_list:
            checkbox.setChecked(False)

    def cheshudanwei_select_all(self):
        for checkbox in self.cheshudanwei_checkbox_list:
            if checkbox.isVisible():
                checkbox.setChecked(True)

    def cheshudanwei_select_none(self):
        for checkbox in self.cheshudanwei_checkbox_list:
            checkbox.setChecked(False)

    def driver_select_all(self):
        for checkbox in self.drivers_checkbox_list:
            if checkbox.isVisible():
                checkbox.setChecked(True)

    def driver_select_none(self):
        for checkbox in self.drivers_checkbox_list:
            checkbox.setChecked(False)

    @staticmethod
    def init_scroll_area(scroll_area, checkbox_desc, checkbox_list):
        content_widget = QtWidgets.QWidget()
        content_widget.setFixedHeight(35 * (len(checkbox_desc) + 1))
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignTop)
        content_widget.setLayout(content_layout)
        for desc in checkbox_desc:
            checkbox = QtWidgets.QCheckBox(desc, parent=scroll_area)
            content_layout.addWidget(checkbox)
            checkbox_list.append(checkbox)
        scroll_area.setWidget(content_widget)

    def driver_search_key_changed(self, k):
        for checkbox in self.drivers_checkbox_list:
            if k in checkbox.text():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
        # 回到顶部
        self.drivers_scroll_area.verticalScrollBar().setValue(0)

    def cheshudanwei_search_key_changed(self, k):
        for checkbox in self.cheshudanwei_checkbox_list:
            if k in checkbox.text():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
        # 回到顶部
        self.cheshudanweis_scroll_area.verticalScrollBar().setValue(0)

    def init_font(self):
        font = QApplication.font()
        self.date_start.setFont(font)
        self.date_end.setFont(font)

    def yongchedanwei_search_key_changed(self, key):
        for checkbox in self.yongchedanwei_checkbox_list:
            if key in checkbox.text():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
        # 回到顶部
        self.yongchedanweis_scroll_area.verticalScrollBar().setValue(0)

    def search_btn_execute_clicked(self):
        # 获取搜索参数
        date_start = self.date_start.date().toString('yyyy-MM-dd')
        date_end = self.date_end.date().toString('yyyy-MM-dd')
        if date_start > date_end:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "开始日期不能大于结束日期！")
            message_box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            message_box.exec_()
            return

        search_args = {
            'date_start': date_start,
            'date_end': date_end,
            'yongchedanweis': set(item.text() for item in self.yongchedanwei_checkbox_list if item.isChecked()),
            'cheshudanweis': set(item.text() for item in self.cheshudanwei_checkbox_list if item.isChecked()),
            'drivers': set(item.text() for item in self.drivers_checkbox_list if item.isChecked()),
            'itinerary': self.itinerary.text(),
            'fu': set(item.text() for item in self.fu_checkbox_list if item.isChecked()),
            'shou': set(item.text() for item in self.shou_checkbox_list if item.isChecked()),
        }
        # 发送信号
        self.search_args_signal.emit(search_args)
