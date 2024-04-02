import asyncio
import time

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QComboBox

from settings import ServiceUri, ServicePort
from utils.excel import export_table_widget, get_sheet_data_and_headers
from utils.qhttp import Http
from utils.qsocketio import SocketIOClient
from widgets.create_user_table_dialog.win import UserTableCreateDialog
from widgets.create_wage_table_dialog.win import WageTableCreateDialog
from widgets.f_s_dialog.win import FSDialog
from widgets.main_table_add_dialog.win import MainTableAddDialog
from widgets.main_table_search_widget.win import MainTableSearchWidget
from widgets.qtable_main_widget.win import QTableMainWindow
from widgets.shared_table_widget.shared_table_widget import Ui_shared_table_widget
from widgets.u_s_dialog.win import USDialog


class SharedTableWin(QtWidgets.QMainWindow, Ui_shared_table_widget):
    add_one_row_success_signal = QtCore.pyqtSignal()
    refresh_table_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(SharedTableWin, self).__init__(parent)

        self.setupUi(self)

        self.key_convert = {
            'record_id': '序号',
            'bz': '备注',
            'ch': '车号',
            'csdw': '车属单位',
            'cx': '车型',
            'fu': '付',
            'je': '金额',
            'jy': '结余',
            'piao': '票',
            'qd': '签单',
            'rq': '日期',
            'shou': '收',
            'sj': '司机',
            'xc': '行程',
            'ycdw': '用车单位',
            'ycsj': '用车时间',
            'yf': '应付'
        }
        self.name_to_key = {v: k for k, v in self.key_convert.items()}
        self.name_to_key['时间'] = 'ycsj'

        self.old_version_key_to_new_version_key = {
            "date": "rq",
            "driver": "sj",
            "car_type": "cx",
            "car_number": "ch",
            "qiandan": "qd",
            "cheshudanwei": "csdw",
            "yongchedanwei": "ycdw",
            "time": "ycsj",
            "money": "je",
            "shou": "shou",
            "pay": "yf",
            "fu": "fu",
            "remark": "bz",
            "pic": "piao",
            "itinerary": "xc",
        }
        self.column_name_to_index = {}

        for i in range(self.tableWidget.columnCount()):
            self.column_name_to_index[self.tableWidget.horizontalHeaderItem(i).text()] = i

        # socketio signal
        self.socketio_client = SocketIOClient(parent=self)  # 这里面的信号要和这里的槽函数绑定
        self.socketio_client.operation_desc_signal.connect(self.log_widget_append)
        self.socketio_client.init_table_data_signal.connect(self.init_table_data)
        self.socketio_client.add_one_row_to_data_center_signal.connect(self.add_one_row_to_data_center_callback)
        self.socketio_client.add_rows_to_data_center_signal.connect(self.add_rows_to_data_center_callback)
        self.socketio_client.delete_rows_from_data_center_signal.connect(self.delete_rows_from_data_center_callback)
        self.socketio_client.update_data_center_signal.connect(self.update_data_center_callback)
        self.socketio_client.all_operation_logs_from_date_signal.connect(self.all_operation_logs_from_date)
        self.socketio_client.error_occurred_signal.connect(self.socketio_connect_error_occurred_slot)
        # menu actions
        self.add_one_row.triggered.connect(self.add_one_row_slot)
        self.add_rows.triggered.connect(self.add_rows_slot)
        self.delete_selected_row.triggered.connect(self.delete_rows_from_data_center)
        self.show_all_data_action.triggered.connect(self.show_all_data_slot)
        self.main_table_search_action.triggered.connect(self.main_table_search_slot)
        self.create_user_table_action.triggered.connect(self.create_user_table_slot)
        self.create_wage_table_action.triggered.connect(self.create_wage_table_slot)
        self.u_s_action.triggered.connect(self.u_s_action_slot)
        self.f_s_action.triggered.connect(self.f_s_action_slot)
        self.user_logout.triggered.connect(self.user_logout_slot)

        self.export_main_table_action.triggered.connect(self.export_main_table_slot)

        self.refresh_table_btn = QtWidgets.QPushButton("重新同步表格数据", self)
        self.menubar.setCornerWidget(self.refresh_table_btn, QtCore.Qt.TopRightCorner)
        self.refresh_table_btn.clicked.connect(self.refresh_table_btn_clicked)

        self.tableWidget.cellClicked.connect(self.table_widget_cell_clicked_slot)

        self.refresh_table_signal.connect(self.refresh_table_signal_slot)

        self.log_search_key_line_edit.textChanged.connect(self.log_search_key_line_edit_text_changed)
        self.clear_log_btn.clicked.connect(lambda: self.logWidget.clear())
        self.logWidget.setWordWrap(True)
        # 行程所在列宽度设置为360
        self.tableWidget.setColumnWidth(self.column_name_to_index['行程'], 320)
        self.tableWidget.setColumnWidth(self.column_name_to_index['用车时间'], 160)

        qd_index = self.column_name_to_index['签单']
        piao_index = self.column_name_to_index['票']
        shou_index = self.column_name_to_index['收']
        fu_index = self.column_name_to_index['付']
        self.check_box_index = {qd_index, piao_index, shou_index, fu_index}
        for index in self.check_box_index:
            self.tableWidget.setColumnWidth(index, 55)

        self.namespace = ["/"]

        self.name = None
        self.username = None
        self.operation_type = None
        self.access_token = None
        self.privilege = None

        self.last_click_pos = (-1, -1)
        self.http = Http()
        self.center()

    def f_s_dialog_args_slot(self, year, months):
        income, income_index = 0, self.column_name_to_index['金额']
        expense, expense_index = 0, self.column_name_to_index['应付']
        balance, balance_index = 0, self.column_name_to_index['结余']
        year_index = self.column_name_to_index['日期']
        months = sorted(months)
        if len(months) == 12:
            # 全年
            headers = [f'{year}年度总收入', f'{year}年度总支出', f'{year}年度结余']
        else:
            headers = [f'{months}月份总收入', f'{months}月份总支出', f'{months}月份总结余']
        flag = False
        rows = []
        for i in range(self.tableWidget.rowCount()):
            year_table, month_table, _ = self.tableWidget.item(i, year_index).text().split('-')
            if year_table != year:
                # 判断年
                continue
            if len(months) != 12 and int(month_table) not in months:
                # 判断月
                continue
            income_str = self.tableWidget.item(i, income_index).text().strip()
            expense_str = self.tableWidget.item(i, expense_index).text().strip()
            balance_str = self.tableWidget.item(i, balance_index).text().strip()
            try:
                income_number = float(income_str if income_str else '0')
                expense_number = float(expense_str if expense_str else '0')
                balance_number = float(balance_str if balance_str else '0')
                # 是负数也抛出异常
            except Exception as e:
                rows.append(self.tableWidget.item(i, 0).text())
                income_number = 0
                expense_number = 0
                balance_number = 0
                flag = True
            income += income_number
            expense += expense_number
            balance += balance_number
        if flag:
            rows = sorted(rows)
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告",
                                  f"序号为{rows}存在非纯数字情况！所在记录不进行计算！", parent=self).exec_()
        self.show_table_data("收支统计表", [[income, expense, balance]], headers)

    def f_s_action_slot(self):
        f_s_dialog = FSDialog(parent=self)
        f_s_dialog.search_signal.connect(self.f_s_dialog_args_slot)
        f_s_dialog.exec_()

    def socketio_connect_error_occurred_slot(self, *args):
        try:
            # 使用线程再次连接
            # threading.Thread(target=self.socketio_client.connect, args=(self.access_token, self.namespace)).start()
            # 使用协程连接
            asyncio.create_task(self.socketio_client.connect(self.access_token, self.namespace))
        except Exception as e:
            print(e)

    def log_search_key_line_edit_text_changed(self, key):
        # 过滤logWidget中的内容
        for i in range(self.logWidget.count()):
            item = self.logWidget.item(i)
            if key in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def all_operation_logs_from_date(self, logs: list):
        self.logWidget.clear()
        # logs逆序
        logs.reverse()
        for log in logs:
            log = log[0]
            self.logWidget.addItem(log + '\n')

    def log_widget_append(self, operation_desc):
        self.logWidget.insertItem(0, operation_desc + '\n')

    def add_rows_to_data_center_callback(self, resp):
        data = resp['data']
        operation_desc = resp['operation_desc']
        self.logWidget.insertItem(0, operation_desc + '\n')
        self.init_table_data(data)

    def add_rows_slot(self):
        # 先判断是否有添加权限
        if self.privilege['can_add'] != '√':
            QtWidgets.QMessageBox.warning(self, "警告", "您没有添加权限！")
            return

        # 这个操作需要打开一个文件选择对话框，选择一个excel文件，然后将数据导入到表格中
        filename, file_type = QtWidgets.QFileDialog.getOpenFileName(self, "选择要导入的文件", "./",
                                                                    "Excel(*.xlsx *.xls *.xlsm)")
        if not filename:
            return
        headers, data = get_sheet_data_and_headers(filename)

        if not headers or not data:
            QtWidgets.QMessageBox.warning(self, "警告", "导入的数据异常，请检查后重试！")
            return

        if len(headers) != self.tableWidget.columnCount() - 1:
            QtWidgets.QMessageBox.warning(self, "警告", "导入的数据列数和表格列数不一致，请检查后重试！")
            return
        # headers转换为新版本的key name_to_key
        for i, header in enumerate(headers):
            if header in self.name_to_key:
                headers[i] = self.name_to_key[header]
            else:
                # 警告数据不符合规范
                QtWidgets.QMessageBox.warning(self, "警告", f"表格中的列名 {header} 不符合规范，请检查后重试！")
                return
        # 询问用户是否继续
        # 需要中文确认和取消
        question_dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "确认导入", "确认导入数据吗？",
                                                parent=self)
        question_dialog.addButton("确认", QtWidgets.QMessageBox.YesRole)
        question_dialog.addButton("取消", QtWidgets.QMessageBox.NoRole)
        reply = question_dialog.exec_()
        # 这里要用0, 1进行判断
        # 0 1 与添加顺序有关
        # YesRole || NoRole 只是判定位置的
        if reply == 1:
            return
        self.socketio_client.sio.emit("c2s_add_rows_to_data_center", {
            "fields": headers,
            "data": data,
            "username": self.username
        })

    def export_main_table_slot(self):
        number_cols = [10, 13, 15]
        filename, file_type = QtWidgets.QFileDialog.getSaveFileName(self, "导出当前数据", "",
                                                                    "Excel(*.xlsx *.xls *.xlsm)")
        if not filename:
            return
        flag, _, = export_table_widget(self.tableWidget, filename, number_cols)
        if flag:
            QtWidgets.QMessageBox.information(self, "导出提示", "导出成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "导出提示", "确保当前打开的文件已被关闭，然后重试！")

    def refresh_table_signal_slot(self, data):
        if data['type'] == 'success':
            # 弹出提示框
            QtWidgets.QMessageBox.information(self, "提示", "表格数据同步成功！")

    def refresh_table_btn_clicked(self):
        if not self.socketio_client.sio.connected:
            # 这里需要同步连接
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.socketio_client.connect(self.access_token, self.namespace))

        # callback主要用来测试回调
        # 可以像http一样，发送请求，然后等待回调
        # 这里要用信号槽连接refresh_table_signal如果直接回调refresh_table_signal_slot并弹出窗口会有问题
        # 弹出窗口会阻塞，导致socketio_client的回调函数无法执行
        # 原因：callback的回调函数本质上是在socketio_client的线程中执行的，不要阻塞
        self.socketio_client.sio.emit("c2s_refresh_table_from_data_center",
                                      namespace='/',
                                      callback=lambda resp: self.refresh_table_signal.emit(resp)
                                      )

    def get_yongchedanwei_from_main_table(self):
        # 获取“用车单位”列表
        index = self.column_name_to_index["用车单位"]
        yongchedanwei_set = set()
        for i in range(self.tableWidget.rowCount()):
            yongchedanwei_set.add(self.tableWidget.item(i, index).text())
        yongchedanwei_set = sorted(yongchedanwei_set)
        return yongchedanwei_set

    def get_cheshudanwei_from_main_table(self):
        # 获取“车属单位”列表
        index = self.column_name_to_index["车属单位"]
        cheshudanwei_set = set()
        for i in range(self.tableWidget.rowCount()):
            cheshudanwei_set.add(self.tableWidget.item(i, index).text())
        cheshudanwei_set = sorted(cheshudanwei_set)
        return cheshudanwei_set

    def get_driver_from_main_table(self):
        # 获取“司机”列表
        index = self.column_name_to_index["司机"]
        driver_set = set()
        for i in range(self.tableWidget.rowCount()):
            driver_set.add(self.tableWidget.item(i, index).text())
        driver_set = sorted(driver_set)
        return driver_set

    def search_args_slot(self, search_args):
        data_start = search_args['date_start']
        date_end = search_args['date_end']
        ycdw = search_args['yongchedanweis']
        csdw = search_args['cheshudanweis']
        sj = search_args['drivers']
        xc = search_args['itinerary']
        fu = search_args['fu']
        shou = search_args['shou']

        data_index = self.column_name_to_index['日期']
        ycdw_index = self.column_name_to_index['用车单位']
        csdw_index = self.column_name_to_index['车属单位']
        sj_index = self.column_name_to_index['司机']
        xc_index = self.column_name_to_index['行程']
        fu_index = self.column_name_to_index['付']
        shou_index = self.column_name_to_index['收']

        # 设置所有行可见
        self.show_all_data_slot()

        for i in range(self.tableWidget.rowCount()):
            data_item = self.tableWidget.item(i, data_index)
            if data_item.text() < data_start or data_item.text() > date_end:
                self.tableWidget.setRowHidden(i, True)
                continue

            ycdw_item = self.tableWidget.item(i, ycdw_index)
            if ycdw:
                if ycdw_item.text() not in ycdw:
                    self.tableWidget.setRowHidden(i, True)
                    continue

            csdw_item = self.tableWidget.item(i, csdw_index)
            if csdw:
                if csdw_item.text() not in csdw:
                    self.tableWidget.setRowHidden(i, True)
                    continue

            sj_item = self.tableWidget.item(i, sj_index)
            if sj and sj_item.text() not in sj:
                self.tableWidget.setRowHidden(i, True)
                continue

            xc_item = self.tableWidget.item(i, xc_index)
            if xc not in xc_item.text():
                self.tableWidget.setRowHidden(i, True)
                continue

            fu_item = self.tableWidget.item(i, fu_index)
            if fu and fu_item.text() not in fu:
                self.tableWidget.setRowHidden(i, True)
                continue

            shou_item = self.tableWidget.item(i, shou_index)
            if shou and shou_item.text() not in shou:
                self.tableWidget.setRowHidden(i, True)
                continue

    def create_user_table_args_slot(self, start_date, end_date, yongchedanweis, fus, shous):
        # 需要 rq, ycdw, ycsj, sj, ch, cx, xc, je, bz
        data_index = self.column_name_to_index['日期']
        ycdw_index = self.column_name_to_index['用车单位']
        ycsj_index = self.column_name_to_index['用车时间']
        sj_index = self.column_name_to_index['司机']
        ch_index = self.column_name_to_index['车号']
        cx_index = self.column_name_to_index['车型']
        xc_index = self.column_name_to_index['行程']
        je_index = self.column_name_to_index['金额']
        bz_index = self.column_name_to_index['备注']
        fu_index = self.column_name_to_index['付']
        shou_index = self.column_name_to_index['收']

        target_data = []
        for i in range(self.tableWidget.rowCount()):
            # if self.tableWidget.isRowHidden(i):
            #     continue
            data_item = self.tableWidget.item(i, data_index)
            if data_item.text() < start_date or data_item.text() > end_date:
                continue
            ycdw_item = self.tableWidget.item(i, ycdw_index)
            if yongchedanweis and ycdw_item.text() not in yongchedanweis:
                continue
            fu_item = self.tableWidget.item(i, fu_index)
            if fus and fu_item.text() not in fus:
                continue
            shou_item = self.tableWidget.item(i, shou_index)
            if shous and shou_item.text() not in shous:
                continue
            # 需要rq, ycdw, ycsj, sj, ch, cx, xc, je, bz
            row = [data_item.text(), ycdw_item.text(), self.tableWidget.item(i, ycsj_index).text(),
                   self.tableWidget.item(i, sj_index).text(), self.tableWidget.item(i, ch_index).text(),
                   self.tableWidget.item(i, cx_index).text(), self.tableWidget.item(i, xc_index).text(),
                   self.tableWidget.item(i, je_index).text(), self.tableWidget.item(i, bz_index).text()]
            target_data.append(row)
        headers = ["日期", "用车单位", "用车时间", "司机", "车号", "车型", "行程", "金额", "备注"]
        number_cols = [7]
        self.show_table_data("客户账单", target_data, headers, number_cols)

    def create_wage_table_args_slot(self, start_date, end_date, driver, cheshudanwei, fus, shous):
        # 从表格中搜索符合条件的行（在可视范围内）
        # 在新的表格中显示，并且带有“导出”按钮
        data_index = self.column_name_to_index['日期']
        sj_index = self.column_name_to_index['司机']
        csdw_index = self.column_name_to_index['车属单位']
        fu_index = self.column_name_to_index['付']
        shou_index = self.column_name_to_index['收']

        ycdw_index = self.column_name_to_index['用车单位']
        xc_index = self.column_name_to_index['行程']
        yf_index = self.column_name_to_index['应付']
        bz_index = self.column_name_to_index['备注']

        target_data = []
        for i in range(self.tableWidget.rowCount()):
            # if self.tableWidget.isRowHidden(i):
            #     continue
            data_item = self.tableWidget.item(i, data_index)
            if data_item.text() < start_date or data_item.text() > end_date:
                continue
            sj_item = self.tableWidget.item(i, sj_index)
            if driver and sj_item.text() != driver:
                continue
            csdw_item = self.tableWidget.item(i, csdw_index)
            if cheshudanwei and csdw_item.text() != cheshudanwei:
                continue
            fu_item = self.tableWidget.item(i, fu_index)
            if fus and fu_item.text() not in fus:
                continue
            shou_item = self.tableWidget.item(i, shou_index)
            if shous and shou_item.text() not in shous:
                continue
            # 需要data, sj, csdw, ycdw, xc, yf, bz
            row = [data_item.text(), sj_item.text(), csdw_item.text(), self.tableWidget.item(i, ycdw_index).text(),
                   self.tableWidget.item(i, xc_index).text(), self.tableWidget.item(i, yf_index).text(),
                   self.tableWidget.item(i, bz_index).text()]
            target_data.append(row)
        headers = ["日期", "司机", "车属单位", "用车单位", "行程", "应付", "备注"]
        number_cols = [5]
        self.show_table_data("工资表", target_data, headers, number_cols)

    def u_s_dialog_args_slot(self, target_year, yongchedanweis):
        yongchedanweis = set(yongchedanweis)
        # 从表格中搜索符合条件的行（在可视范围内）
        # 生成的header为“用车单位”，“月份”，“收入”，“支出”，“结余”
        je_index = self.column_name_to_index['金额']
        yf_index = self.column_name_to_index['应付']
        jy_index = self.column_name_to_index['结余']
        ycdw_index = self.column_name_to_index['用车单位']
        data_index = self.column_name_to_index['日期']
        data = {}
        for yongchedanwei in yongchedanweis:
            data[yongchedanwei] = {str(i): [0, 0, 0] for i in range(1, 13)}
        # 每一个是{} key是月份，value是[income, expense, balance]
        for i in range(self.tableWidget.rowCount()):
            # if self.tableWidget.isRowHidden(i):
            #     continue
            date = self.tableWidget.item(i, data_index).text()
            year, month, day = date.split('-')
            if target_year != year:
                continue
            yongchedanwei = self.tableWidget.item(i, ycdw_index).text()
            if yongchedanwei not in yongchedanweis:
                continue
            month = month.lstrip('0')
            income = self.tableWidget.item(i, je_index).text()
            expense = self.tableWidget.item(i, yf_index).text()
            balance = self.tableWidget.item(i, jy_index).text()
            try:
                data[yongchedanwei][month][0] += float(income)
                data[yongchedanwei][month][1] += float(expense)
                data[yongchedanwei][month][2] += float(balance)
            except Exception as e:
                pass
        target_data = []
        for yongchedanwei in yongchedanweis:
            for month in range(1, 13):
                month = str(month)
                income, expense, balance = data[yongchedanwei][month]
                target_data.append([yongchedanwei, month, income, expense, balance])
        self.show_table_data("客户账单统计表", target_data, ["用车单位", "月份", "收入", "支出", "结余"], [2, 3, 4])

    def show_table_data(self, title, data, headers, number_cols=None):
        qTableMainWindow = QTableMainWindow(title, headers, data, number_cols, parent=self)
        qTableMainWindow.show()

    def main_table_search_slot(self):
        yongchedanwei_set = self.get_yongchedanwei_from_main_table()
        cheshudanwei_set = self.get_cheshudanwei_from_main_table()
        driver_set = self.get_driver_from_main_table()
        fu_set = {'√', '×', ''}
        shou_set = {'√', '×', ''}
        dialog = MainTableSearchWidget(yongchedanwei_set, cheshudanwei_set, driver_set, fu_set, shou_set, self)
        dialog.search_args_signal.connect(self.search_args_slot)
        dialog.exec_()

    def create_user_table_slot(self):
        # 打开用户表创建窗口
        yongchedanweis = self.get_yongchedanwei_from_main_table()
        fus = {'√', '×', ''}
        shous = {'√', '×', ''}
        user_table_create_dialog = UserTableCreateDialog(yongchedanweis, fus, shous, parent=self)
        user_table_create_dialog.create_user_table_args_signal.connect(self.create_user_table_args_slot)
        user_table_create_dialog.show()

    def create_wage_table_slot(self):
        driver_set = self.get_driver_from_main_table()
        cheshudanwei_set = self.get_cheshudanwei_from_main_table()
        fu_set = {'√', '×', ''}
        shou_set = {'√', '×', ''}
        wage_table_create_dialog = WageTableCreateDialog(driver_set, cheshudanwei_set, fu_set, shou_set, parent=self)
        wage_table_create_dialog.search_signal.connect(self.create_wage_table_args_slot)
        wage_table_create_dialog.show()

    def u_s_action_slot(self):
        yongchedanweis = self.get_yongchedanwei_from_main_table()
        u_s_dialog = USDialog(yongchedanweis, parent=self)
        u_s_dialog.search_signal.connect(self.u_s_dialog_args_slot)
        u_s_dialog.show()

    def show_all_data_slot(self):
        # 设置所有行可见
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(i, False)

    def closeEvent(self, e):
        # 清空服务器端的access_token
        if self.access_token:
            url = f"{ServiceUri}:{ServicePort}/user/logout"
            headers = {
                "Authorization": self.access_token
            }
            params = {}
            self.http.get(url, params, headers)

        time.sleep(0.3)



    def user_logout_slot(self):
        self.close()

    def after_login(self, username, name, operation_type, access_token, privilege):
        try:
            # 使用线程连接
            # threading.Thread(target=self.socketio_client.connect, args=(access_token, self.namespace)).start()
            # 使用协程连接 注意asyncqt的QEventLoop
            asyncio.create_task(self.socketio_client.connect(access_token, self.namespace))
            # 多线程中使用asyncio.run_coroutine_threadsafe
        except Exception as e:
            print(e)
        self.show()
        self.username = username
        self.name = name
        self.operation_type = operation_type
        self.access_token = access_token
        self.privilege = privilege
        # 设置statusbar的提示
        self.statusbar.showMessage(f"欢迎您，{name}。")

    def delete_rows_from_data_center_callback(self, resp):
        try:
            self.tableWidget.cellChanged.disconnect(self.cell_changed_slot)
        except Exception as e:
            pass
        deleted_record_ids = set(resp['record_ids'])
        operation_desc = resp['operation_desc']

        # 删除表格中的行
        # 这里要注意，删除的时候要从后往前删除，否则删除后的行号会变化
        rows_to_delete = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() in deleted_record_ids:
                rows_to_delete.append(i)
        rows_to_delete.sort(reverse=True)
        for row in rows_to_delete:
            self.tableWidget.removeRow(row)

        self.logWidget.insertItem(0, operation_desc + '\n')
        self.tableWidget.cellChanged.connect(self.cell_changed_slot)

    def delete_rows_from_data_center(self):
        # 先判断是否有删除权限
        if self.privilege['can_delete'] != '√':
            QtWidgets.QMessageBox.warning(self, "警告", "您没有删除权限！")
            return

        record_ids = []
        selected_ranges = self.tableWidget.selectedRanges()
        # 可能存在多个选中区域，record_id可能重复
        for selected_range in selected_ranges:
            top_row = selected_range.topRow()
            bottom_row = selected_range.bottomRow() + 1
            for row in range(top_row, bottom_row):
                record_id = self.tableWidget.item(row, 0).text()
                record_ids.append(record_id)

        if len(record_ids) == 0:
            # 警告
            QtWidgets.QMessageBox.warning(self, "警告", "请先选择要删除的行")
            return
        # 询问用户是否继续
        # 需要中文确认和取消
        question_dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "确认删除", "确认删除选中的行吗？",
                                                parent=self)
        question_dialog.addButton("确认", QtWidgets.QMessageBox.YesRole)
        question_dialog.addButton("取消", QtWidgets.QMessageBox.NoRole)
        reply = question_dialog.exec_()
        if reply == 1:
            return
        record_ids = list(set(record_ids))
        self.socketio_client.sio.emit("c2s_delete_rows_from_data_center", {
            "record_ids": record_ids,
            "username": self.username
        })

    def update_data_center_callback(self, resp):
        record_id = str(resp['record_id'])
        key = resp['field']
        value = resp['value']
        operation_desc = resp['operation_desc']
        try:
            self.tableWidget.cellChanged.disconnect(self.cell_changed_slot)
        except Exception as e:
            pass
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() == record_id:
                self.tableWidget.item(i, self.column_name_to_index[self.key_convert[key]]).setText(value)
                if key == 'je' or key == 'yf':
                    try:
                        je = float(self.tableWidget.item(i, self.column_name_to_index['金额']).text())
                        yf = float(self.tableWidget.item(i, self.column_name_to_index['应付']).text())
                        jy = je - yf
                        self.tableWidget.item(i, self.column_name_to_index['结余']).setText(str(jy))
                    except Exception as e:
                        pass
                break

        self.logWidget.insertItem(0, operation_desc + '\n')
        self.tableWidget.cellChanged.connect(self.cell_changed_slot)

    def cell_changed_slot(self, row, column):
        # 更新数据中心的内容
        # print("检测到数据发生变化：", row, column)
        record_id = self.tableWidget.item(row, 0).text()
        key = self.name_to_key[self.tableWidget.horizontalHeaderItem(column).text()]
        value = self.tableWidget.item(row, column).text()
        value = value.strip()
        self.socketio_client.sio.emit("c2s_update_data_center", {
            "record_id": record_id,
            "field": key,
            "value": value,
            "username": self.username
        })

    def add_one_row_to_data_center_callback(self, resp):
        self.add_one_row_success_signal.emit()
        try:
            self.tableWidget.cellChanged.disconnect(self.cell_changed_slot)
        except Exception as e:
            pass

        data = resp['add_info']
        operation_desc = resp['operation_desc']

        # 插入到表格
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        for key, value in data.items():
            key = self.key_convert[key]
            self.tableWidget.setItem(row, self.column_name_to_index[key], QtWidgets.QTableWidgetItem(str(value)))
        self.logWidget.insertItem(0, operation_desc + '\n')

        self.disable_column()

        self.tableWidget.cellChanged.connect(self.cell_changed_slot)

    def add_one_row_to_data_center(self, add_info):
        convert_add_info = {}
        for key, value in add_info.items():
            convert_add_info[self.old_version_key_to_new_version_key[key]] = value
        je = float(add_info['money'])
        yf = float(add_info['pay'])
        jy = je - yf
        convert_add_info['jy'] = jy
        convert_add_info['piao'] = ''
        self.socketio_client.sio.emit("c2s_add_one_row_to_data_center", {
            "add_info": convert_add_info,
            "username": self.username
        })

    def add_one_row_slot(self):
        # 先判断是否有权限
        if self.privilege['can_add'] != '√':
            QtWidgets.QMessageBox.warning(self, "警告", "您没有添加权限！")
            return

        dialog = MainTableAddDialog(self)
        dialog.add_confirm.connect(self.add_one_row_to_data_center)
        self.add_one_row_success_signal.connect(dialog.add_completed_slot)
        dialog.exec_()

    def combo_box_current_text_changed(self, row, column, text):
        # 编辑完成以后，将QComboBox销毁，将值写入单元格
        self.tableWidget.removeCellWidget(row, column)
        self.last_click_pos = (-1, -1)
        item = self.tableWidget.item(row, column)
        item.setText(text)

    def table_widget_cell_clicked_slot(self, row, column):
        # print("单元格被点击：", row, column)
        if self.last_click_pos[0] != -1:
            self.tableWidget.removeCellWidget(self.last_click_pos[0], self.last_click_pos[1])
            self.last_click_pos = (-1, -1)
        # 下面四列需要QComboBox {'√', '×', ''}
        if column not in self.check_box_index:
            return
        # 判断对应的权限
        column_name = self.tableWidget.horizontalHeaderItem(column).text()
        key = self.name_to_key[column_name]
        if self.privilege[key] != '√':
            return

        self.last_click_pos = (row, column)
        # 该单元格无法直接编辑，需要弹出QComboBox
        # 设置无法编辑
        item = self.tableWidget.item(row, column)
        # 设置QComboBox 并自动展开
        combo_box = QComboBox()
        combo_box.addItems(['√', '×', ''])
        combo_box.setCurrentText(item.text())
        self.tableWidget.setCellWidget(row, column, combo_box)
        combo_box.showPopup()
        # 编辑完成以后，将QComboBox销毁，将值写入单元格
        combo_box.currentTextChanged.connect(lambda text: self.combo_box_current_text_changed(row, column, text))

    # 表格第一列是序号，不允许编辑，但是允许选中
    def disable_column(self):
        # 设置第一列不可编辑
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        # 根据权限设置其他列是否可编辑
        # 权限是一个字典，key是列名（需要key_convert一下），value为是否可编辑只有'√'可以编辑
        try:
            for i in range(1, self.tableWidget.columnCount()):
                column_name = self.tableWidget.horizontalHeaderItem(i).text()
                key = self.name_to_key[column_name]
                if self.privilege[key] == '√':
                    for j in range(self.tableWidget.rowCount()):
                        item = self.tableWidget.item(j, i)
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
                else:
                    for j in range(self.tableWidget.rowCount()):
                        item = self.tableWidget.item(j, i)
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        except Exception as e:
            print(e)



    def init_table_data(self, data):
        try:
            self.tableWidget.cellChanged.disconnect(self.cell_changed_slot)
        except Exception as e:
            pass

        self.tableWidget.setRowCount(len(data))

        for i, row in enumerate(data):
            for key, value in row.items():
                key = self.key_convert[key]
                column_index = self.column_name_to_index[key]
                self.tableWidget.setItem(i, column_index, QtWidgets.QTableWidgetItem(str(value)))
            # 设置为可见
            self.tableWidget.setRowHidden(i, False)
        # 根据日期进行降序
        self.tableWidget.sortItems(self.column_name_to_index['日期'], QtCore.Qt.AscendingOrder)
        # 根据权限设置是否可编辑
        self.disable_column()

        # 设置表格内容fit 除了上面已经设置过的
        for i in range(self.tableWidget.columnCount()):
            if (i in self.check_box_index or i == self.column_name_to_index['行程']
                    or i == self.column_name_to_index['用车时间']):
                continue
            self.tableWidget.resizeColumnToContents(i)

        # resizeRowToContents
        # self.tableWidget.resizeRowsToContents()

        self.tableWidget.cellChanged.connect(self.cell_changed_slot)

    def center(self):
        # 居中显示 且占据屏幕80%
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
