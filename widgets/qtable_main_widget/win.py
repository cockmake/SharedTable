from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

from utils.excel import export_table_widget
from widgets.qtable_main_widget.qtable_main_widget import Ui_qtable_main_widget


class QTableMainWindow(QtWidgets.QMainWindow, Ui_qtable_main_widget):
    def __init__(self, title, headers, data, number_cols=None, parent=None):
        super(QTableMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.tableWidget.set_headers_and_data(headers, data)

        self.export_current_data_action.triggered.connect(self.export_current_data)
        self.number_cols = number_cols

        self.center()

    def export_current_data(self):
        filename, file_type = QtWidgets.QFileDialog.getSaveFileName(self, "导出当前数据", "",
                                                                    "Excel(*.xlsx *.xls *.xlsm)")
        if not filename:
            return
        flag, _, = export_table_widget(self.tableWidget, filename, self.number_cols)
        if flag:
            QtWidgets.QMessageBox.information(self, "导出提示", "导出成功！")
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "导出提示", "确保当前打开的文件已被关闭，然后重试！")

    def center(self):
        # 居中显示 且占据屏幕65%
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() * 0.65, screen.height() * 0.65)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
