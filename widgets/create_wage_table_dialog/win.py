from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from widgets.create_wage_table_dialog.wage_table_dialog import Ui_wage_table_dialog


class WageTableCreateDialog(QtWidgets.QDialog, Ui_wage_table_dialog):
    search_signal = pyqtSignal(str, str, str, str, set, set)

    def __init__(self, driver_set, cheshudanwei_set, fu_set, shou_set, parent=None):
        super(WageTableCreateDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.wage_table_dialog_cancel_btn.clicked.connect(self.close)
        self.wage_table_dialog_search_btn.clicked.connect(self.search_emit)
        self.wage_table_dialog_search_btn.setFocus()
        self.wage_table_end_date.setDate(QtCore.QDate.currentDate())
        # 按列添加radio button到drivers
        widget_content = QtWidgets.QWidget(self)
        layout_content = QtWidgets.QVBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setAlignment(Qt.AlignTop)
        widget_content.setFixedHeight(35 * len(driver_set))
        widget_content.setLayout(layout_content)
        self.driver_radio_button_list = []
        for driver in driver_set:
            radio_button = QtWidgets.QRadioButton(driver, parent=self.drivers)
            layout_content.addWidget(radio_button)
            self.driver_radio_button_list.append(radio_button)
        self.drivers.setWidget(widget_content)
        # 按列添加radio button到cheshudanweis
        widget_content = QtWidgets.QWidget(self)
        layout_content = QtWidgets.QVBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setAlignment(Qt.AlignTop)
        widget_content.setFixedHeight(35 * (len(cheshudanwei_set) + 1))
        widget_content.setLayout(layout_content)
        self.cheshudanwei_radio_button_list = []
        for cheshudanwei in cheshudanwei_set:
            radio_button = QtWidgets.QRadioButton(cheshudanwei, parent=self.cheshudanweis)
            layout_content.addWidget(radio_button)
            self.cheshudanwei_radio_button_list.append(radio_button)
        self.cheshudanweis.setWidget(widget_content)
        # 为drivers_key监听输入框的改变来动态过滤drivers
        self.drivers_key.textChanged.connect(self.drivers_key_changed)
        self.cheshudanweis_key.textChanged.connect(self.cheshudanweis_key_changed)

        # 添加fu shou checkbox到fu_groupbox shou_groupbox
        fu_layout = QtWidgets.QVBoxLayout()
        fu_layout.setAlignment(Qt.AlignTop)
        self.fu_groupbox.setLayout(fu_layout)
        self.fu_checkbox_list = []
        for fu in fu_set:
            checkbox = QtWidgets.QCheckBox(fu)
            fu_layout.addWidget(checkbox)
            self.fu_checkbox_list.append(checkbox)
        shou_layout = QtWidgets.QVBoxLayout()
        shou_layout.setAlignment(Qt.AlignTop)
        self.shou_groupbox.setLayout(shou_layout)
        self.shou_checkbox_list = []
        for shou in shou_set:
            checkbox = QtWidgets.QCheckBox(shou)
            shou_layout.addWidget(checkbox)
            self.shou_checkbox_list.append(checkbox)

    def search_emit(self):
        start_date = self.wage_table_start_date.date().toString("yyyy-MM-dd")
        end_date = self.wage_table_end_date.date().toString("yyyy-MM-dd")
        if start_date > end_date:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "开始日期不能大于结束日期！")
            message_box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            message_box.exec_()
            return
        driver = ""
        for radio_button in self.driver_radio_button_list:
            if radio_button.isChecked():
                driver = radio_button.text()
                break
        cheshudanwei = ""
        for radio_button in self.cheshudanwei_radio_button_list:
            if radio_button.isChecked():
                cheshudanwei = radio_button.text()
                break

        fus = set(checkbox.text() for checkbox in self.fu_checkbox_list if checkbox.isChecked())
        shous = set(checkbox.text() for checkbox in self.shou_checkbox_list if checkbox.isChecked())
        self.search_signal.emit(start_date, end_date, driver, cheshudanwei, fus, shous)

    def drivers_key_changed(self, k):
        for radio_button in self.driver_radio_button_list:
            if k in radio_button.text():
                radio_button.setVisible(True)
            else:
                radio_button.setVisible(False)
        # 回到顶部
        self.drivers.verticalScrollBar().setValue(0)

    def cheshudanweis_key_changed(self, k):
        for radio_button in self.cheshudanwei_radio_button_list:
            if k in radio_button.text():
                radio_button.setVisible(True)
            else:
                radio_button.setVisible(False)
        # 回到顶部
        self.cheshudanweis.verticalScrollBar().setValue(0)
