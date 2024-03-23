from functools import cached_property

import socketio
from PyQt5.QtCore import pyqtSignal, QObject

from settings import SocketIOPort, SocketIOUri


class SocketIOClient(QObject):
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()
    error_occurred_signal = pyqtSignal(object)
    init_table_data_signal = pyqtSignal(list)
    add_one_row_to_data_center_signal = pyqtSignal(dict)
    add_rows_to_data_center_signal = pyqtSignal(dict)
    delete_rows_from_data_center_signal = pyqtSignal(dict)
    operation_desc_signal = pyqtSignal(str)
    update_data_center_signal = pyqtSignal(dict)
    all_operation_logs_from_date_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sio.on("connect", self._handle_connect)
        self.sio.on("disconnect", self._handle_disconnect)
        self.sio.on("connect_error", self._handle_connect_error)

        self.sio.on("s2c_init_table_data", self.init_table_data)
        self.sio.on("s2c_add_one_row_to_data_center", self.add_one_row_to_data_center)
        self.sio.on("s2c_delete_rows_from_data_center", self.s2c_delete_rows_from_data_center)
        self.sio.on("s2c_operation_desc", self.s2c_operation_desc)
        self.sio.on("s2c_add_rows_to_data_center", self.add_rows_to_data_center)
        self.sio.on("s2c_update_data_center", self.update_data_center)
        self.sio.on("s2c_all_operation_logs_from_date", self.all_operation_logs_from_date)

    @cached_property
    def sio(self):
        return socketio.Client(
            # reconnection_attempts=3,
            # reconnection_delay=5,
            # reconnection_delay_max=5
        )

    def stop(self):
        self.sio.disconnect()

    def connect(self, access_token, namespace):
        self.sio.connect(f"{SocketIOUri}:{SocketIOPort}",
                         headers={"Authorization": access_token},
                         transports=["websocket"], namespaces=namespace)

    def _handle_connect(self):
        print("连接成功")
        self.connected_signal.emit()

    def _handle_disconnect(self):
        print("断开连接")
        self.disconnected_signal.emit()

    def _handle_connect_error(self, data):
        print("连接错误")
        self.error_occurred_signal.emit(data)

    def init_table_data(self, data):
        self.init_table_data_signal.emit(data)

    def add_one_row_to_data_center(self, data):
        self.add_one_row_to_data_center_signal.emit(data)

    def s2c_delete_rows_from_data_center(self, data):
        self.delete_rows_from_data_center_signal.emit(data)

    def s2c_operation_desc(self, operation_desc):
        self.operation_desc_signal.emit(operation_desc)

    def add_rows_to_data_center(self, data):
        self.add_rows_to_data_center_signal.emit(data)

    def update_data_center(self, data):
        self.update_data_center_signal.emit(data)

    def all_operation_logs_from_date(self, data):
        self.all_operation_logs_from_date_signal.emit(data)