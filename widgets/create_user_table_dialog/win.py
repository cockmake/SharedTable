from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from widgets.create_user_table_dialog.user_table_dialog import Ui_user_table_dialog


class UserTableCreateDialog(QtWidgets.QDialog, Ui_user_table_dialog):
    create_user_table_args_signal = pyqtSignal(str, str, set, set, set)

    def __init__(self, checkbox_text_list, fu_text_list, shou_text_list, parent=None):
        super(UserTableCreateDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.user_table_create_btn.setFocus()
        self.user_table_end_date.setDate(QtCore.QDate.currentDate())
        self.user_table_cancel_btn.clicked.connect(self.close)
        self.yongchedanwei_search_key.textChanged.connect(self.yongchedanwei_search_key_changed)
        # 按列添加checkbox
        widget_content = QtWidgets.QWidget(self)
        layout_content = QtWidgets.QVBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setAlignment(Qt.AlignTop)
        widget_content.setFixedHeight(35 * (len(checkbox_text_list) + 1))
        widget_content.setLayout(layout_content)
        self.checkbox_list = []
        for desc in checkbox_text_list:
            checkbox = QtWidgets.QCheckBox(desc, parent=self.yongchedanweis)
            layout_content.addWidget(checkbox)
            self.checkbox_list.append(checkbox)
        self.yongchedanweis.setWidget(widget_content)
        # 按钮事件
        self.user_table_create_btn.clicked.connect(self.user_table_create_btn_clicked)

        self.fu_checkbox_list = []
        self.shou_checkbox_list = []

        # 添加fu shou checkbox到groupbox
        fu_layout = QtWidgets.QVBoxLayout()
        fu_layout.setAlignment(Qt.AlignTop)
        self.fu_groupbox.setLayout(fu_layout)
        for desc in fu_text_list:
            checkbox = QtWidgets.QCheckBox(desc, parent=self.fu_groupbox)
            fu_layout.addWidget(checkbox)
            self.fu_checkbox_list.append(checkbox)
        shou_layout = QtWidgets.QVBoxLayout()
        shou_layout.setAlignment(Qt.AlignTop)
        self.shou_groupbox.setLayout(shou_layout)
        for desc in shou_text_list:
            checkbox = QtWidgets.QCheckBox(desc, parent=self.shou_groupbox)
            shou_layout.addWidget(checkbox)
            self.shou_checkbox_list.append(checkbox)

        self.yongchedanwei_select_all_btn.clicked.connect(self.yongchedanwei_select_all)
        self.yongchedanwei_select_none_btn.clicked.connect(self.yongchedanwei_select_none)

    def yongchedanwei_select_all(self):
        for checkbox in self.checkbox_list:
            if checkbox.isVisible():
                checkbox.setChecked(True)

    def yongchedanwei_select_none(self):
        for checkbox in self.checkbox_list:
            checkbox.setChecked(False)

    def yongchedanwei_search_key_changed(self, k):
        for checkbox in self.checkbox_list:
            if k in checkbox.text():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
        # 回到顶部
        self.yongchedanweis.verticalScrollBar().setValue(0)

    def user_table_create_btn_clicked(self):
        start_date = self.user_table_start_date.date().toString("yyyy-MM-dd")
        end_date = self.user_table_end_date.date().toString("yyyy-MM-dd")
        if start_date > end_date:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "开始日期不能大于结束日期！")
            message_box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            message_box.exec_()
            return
        checked_checkbox_text_set = set(checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked())
        fu_checked_set = set(checkbox.text() for checkbox in self.fu_checkbox_list if checkbox.isChecked())
        shou_checked_set = set(checkbox.text() for checkbox in self.shou_checkbox_list if checkbox.isChecked())
        self.create_user_table_args_signal.emit(start_date, end_date, checked_checkbox_text_set, fu_checked_set,
                                                shou_checked_set)
