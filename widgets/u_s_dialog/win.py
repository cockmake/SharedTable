from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QCheckBox

from widgets.u_s_dialog.u_s_dialog import Ui_u_s_dialog


class USDialog(QDialog, Ui_u_s_dialog):
    search_signal = pyqtSignal(str, list)

    def __init__(self, yongchedanweis, parent=None):
        super(USDialog, self).__init__(parent)
        self.setupUi(self)
        self.year.setDate(QtCore.QDate.currentDate())
        self.confirm.setFocus()
        self.confirm.clicked.connect(self.search_emit)
        self.cancel.clicked.connect(self.close)
        # 用车单位
        self.yongchedanwei_checkboxs = []
        widget_content = QtWidgets.QWidget(self)
        layout_content = QtWidgets.QVBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setAlignment(Qt.AlignTop)
        widget_content.setFixedHeight(35 * (len(yongchedanweis) + 1))
        widget_content.setLayout(layout_content)
        for yongchedanwei in yongchedanweis:
            yongchedanwei_checkbox = QCheckBox(yongchedanwei, parent=self.yongchedanweis)
            layout_content.addWidget(yongchedanwei_checkbox)
            self.yongchedanwei_checkboxs.append(yongchedanwei_checkbox)
        self.yongchedanweis.setWidget(widget_content)

        self.search_key.textChanged.connect(self.search_key_changed)

        self.yongchedanwei_select_all_btn.clicked.connect(self.yongchedanwei_select_all)
        self.yongchedanwei_select_none_btn.clicked.connect(self.yongchedanwei_select_none)

    def yongchedanwei_select_all(self):
        for yongchedanwei_checkbox in self.yongchedanwei_checkboxs:
            if yongchedanwei_checkbox.isVisible():
                yongchedanwei_checkbox.setChecked(True)

    def yongchedanwei_select_none(self):
        for yongchedanwei_checkbox in self.yongchedanwei_checkboxs:
            yongchedanwei_checkbox.setChecked(False)

    def search_key_changed(self, k):
        for yongchedanwei_checkbox in self.yongchedanwei_checkboxs:
            if k in yongchedanwei_checkbox.text():
                yongchedanwei_checkbox.setVisible(True)
            else:
                yongchedanwei_checkbox.setVisible(False)

    def search_emit(self):
        yongchedanweis = []
        for yongchedanwei_checkbox in self.yongchedanwei_checkboxs:
            if yongchedanwei_checkbox.isChecked():
                yongchedanweis.append(yongchedanwei_checkbox.text())
        if len(yongchedanweis) == 0:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "请选择用车单位！")
            message_box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            message_box.exec_()
            return
        year = self.year.date().toString("yyyy")
        self.search_signal.emit(year, yongchedanweis)
