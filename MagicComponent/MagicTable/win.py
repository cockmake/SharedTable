from PyQt5 import QtWidgets, QtCore

from MagicComponent.TableColumnCondition import TableColumnCondition


class MagicTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(MagicTable, self).__init__(parent=parent)
        self.horizontalHeader().sectionDoubleClicked.connect(self.onSectionDoubleClicked)
        self.horizontalHeader().sectionClicked.connect(self.onSectionClicked)

        self.currentOrder = QtCore.Qt.DescendingOrder

    def get_data_from_column(self, column):
        data = set()
        for row in range(self.rowCount()):
            data.add(self.item(row, column).text())
        return sorted(data)

    def onSectionDoubleClicked(self, index):
        # 对这一列进行排序 并对排序的箭头进行设置 每次排序翻转一下
        # 异或操作
        self.currentOrder ^= 1
        self.sortItems(index, self.currentOrder)

    def onSectionClicked(self, index):
        title = self.horizontalHeaderItem(index).text()
        data_list = self.get_data_from_column(index)
        table_column_condition = TableColumnCondition(index, title, data_list, parent=self)
        table_column_condition.search_condition_signal.connect(self.search_condition_signal_slot)
        table_column_condition.exec_()

    def search_condition_signal_slot(self, column_index, data_list):
        for row in range(self.rowCount()):
            if self.item(row, column_index).text() in data_list:
                self.showRow(row)
            else:
                self.hideRow(row)

    def set_headers_and_data(self, header, data):
        self.setColumnCount(len(header))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(header)
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(cell)))

        self.resizeColumnsToContents()
