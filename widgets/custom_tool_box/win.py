from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from widgets.custom_tool_box.custom_tool_box import Ui_custom_tool_box


class FunctionToolBox(QtWidgets.QToolBox, Ui_custom_tool_box):
    def __init__(self, parent=None):
        super(FunctionToolBox, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.hide()
