from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from MagicComponent.TableColumnCondition.table_column_condition import Ui_table_column_condition


class TableColumnCondition(QDialog, Ui_table_column_condition):
    search_condition_signal = pyqtSignal(int, set)

    def __init__(self, column_index, title, data_list, parent=None):
        super(TableColumnCondition, self).__init__(parent=parent)
        self.setupUi(self)
        self.groupBox.setTitle(title)
        self.cancel.clicked.connect(self.close)
        self.confirm.clicked.connect(self.confirm_clicked)
        self.column_index = column_index
        item_widget = QtWidgets.QWidget()
        item_widget.setFixedHeight(35 * (len(data_list) + 1))
        item_layout = QtWidgets.QVBoxLayout()
        item_layout.setAlignment(QtCore.Qt.AlignTop)
        item_widget.setLayout(item_layout)
        self.checkbox_list = []
        for data in data_list:
            checkbox = QtWidgets.QCheckBox(data)
            item_layout.addWidget(checkbox)
            self.checkbox_list.append(checkbox)
        self.scroll_area.setWidget(item_widget)
        self.search_key.textChanged.connect(self.search_key_changed)
        self.select_all.clicked.connect(self.select_all_clicked)
        self.not_select_all.clicked.connect(self.not_select_all_clicked)

    def confirm_clicked(self):
        data_list = set()
        for checkbox in self.checkbox_list:
            if checkbox.isChecked():
                data_list.add(checkbox.text())
        self.search_condition_signal.emit(self.column_index, data_list)

    def search_key_changed(self, k):
        for checkbox in self.checkbox_list:
            if k in checkbox.text():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
        # 回到顶部
        self.scroll_area.verticalScrollBar().setSliderPosition(0)

    def not_select_all_clicked(self):
        if self.not_select_all.isChecked():
            self.select_all.setChecked(False)
            for checkbox in self.checkbox_list:
                checkbox.setChecked(False)

    def select_all_clicked(self):
        if self.select_all.isChecked():
            self.not_select_all.setChecked(False)
            for checkbox in self.checkbox_list:
                checkbox.setChecked(True)
