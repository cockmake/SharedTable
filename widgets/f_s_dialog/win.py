from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCheckBox

from widgets.f_s_dialog.f_s_dialog import Ui_f_s_dialog


class FSDialog(QtWidgets.QDialog, Ui_f_s_dialog):
    search_signal = pyqtSignal(str, list)

    def __init__(self, parent=None):
        super(FSDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.year.setDate(QtCore.QDate.currentDate())
        self.confirm.setFocus()
        self.months_checkboxes = []
        # months是scrollArea
        widget_content = QtWidgets.QWidget(self)
        layout_content = QtWidgets.QVBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setAlignment(Qt.AlignTop)
        widget_content.setFixedHeight(35 * 13)
        widget_content.setLayout(layout_content)
        month_all = QCheckBox("全月份", parent=self.months)
        self.months_checkboxes.append(month_all)
        layout_content.addWidget(month_all)
        for i in range(1, 13):
            month = QCheckBox(str(i) + "月", parent=self.months)
            self.months_checkboxes.append(month)
            layout_content.addWidget(month)
        self.months.setWidget(widget_content)

        self.cancel.clicked.connect(self.close)
        self.confirm.clicked.connect(self.search_emit)

    def search_emit(self):
        year = self.year.date().toString("yyyy")
        months = []
        if self.months_checkboxes[0].isChecked():
            months.append("0")
        else:
            for i in range(1, len(self.months_checkboxes)):
                if self.months_checkboxes[i].isChecked():
                    months.append(str(i).strip('月'))
        if len(months) == 0:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "请选择月份！")
            message_box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            message_box.exec_()
            return
        self.search_signal.emit(year, months)
