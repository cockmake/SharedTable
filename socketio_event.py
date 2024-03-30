# socketio配置
import time

import redis
from flask import request
from flask_socketio import SocketIO

from flask_app import app
from persistence import mysql_op, redis_pool
from request_wrap import login_require
from utils.common import get_operation_description

# namespace的含义是把不同的事件定义在不同的命名空间下，这样可以更好的管理事件
# client的连接可以一次性连接多个namespace
# 可以添加验证设置

socketio = SocketIO(app, cors_allowed_origins="*")


# @socketio.on('connect', namespace='/a')
@socketio.on('connect', namespace='/')
@login_require
def handle_connect(uname, name):
    print('客户端连接成功')
    # 如何拒绝连接
    # 直接 return False

    # 一般并不在这里初始化数据，而是在命名空间下的另外一个事件中初始化
    # 因为client可以连接多个命名空间，无法确定发往哪个命名空间
    socketio.emit('s2c_init_table_data',
                  mysql_op.get_table_from_data_center(),
                  to=request.sid, namespace='/')

    # 将登录信息发送除了自己以外的前端（因为下面会同步所有的操作日志，只有其他客户端需要这条信息）
    login_desc = get_operation_description(name, "登录", [])
    socketio.emit('s2c_operation_desc', login_desc, include_self=False)
    # 自己同步今天所有的操作日志
    today = time.strftime("%Y-%m-%d", time.localtime())
    socketio.emit('s2c_all_operation_logs_from_date', mysql_op.get_all_operation_logs_from_date(today),
                  to=request.sid, namespace='/')
    # print("*" * 20)


@socketio.on('disconnect')
def handle_disconnect():
    pass
    # print('客户端断开连接')
    # print("*" * 20)


@socketio.on('c2s_add_one_row_to_data_center')
@login_require
def handle_add_one_row_to_data_center(uname, name, data):
    # 判断该token是否有权限添加can_add
    auth = request.headers.get('Authorization', '')
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        privilege = redis_op.hget(auth, "can_add")
    if privilege is None or privilege == '×':
        return
    # username是装饰器传递进来的
    # data是前端传递进来的
    add_info = data.get('add_info', {})
    username = data.get('username', '')
    if not add_info or username != uname:
        return
    add_info, operation_desc = mysql_op.add_one_row_to_data_center(add_info, username, name)
    if not operation_desc.endswith("错误"):
        socketio.emit('s2c_add_one_row_to_data_center', {
            "add_info": add_info,
            "operation_desc": operation_desc
        })
    else:
        socketio.emit('s2c_operation_desc', operation_desc)
    # print("*" * 20)


@socketio.on('c2s_delete_rows_from_data_center')
@login_require
def handle_delete_rows_from_data_center(uname, name, data):
    # 判断该token是否有权限删除can_delete
    auth = request.headers.get('Authorization', '')
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        privilege = redis_op.hget(auth, "can_delete")
    if privilege is None or privilege == '×':
        return

    record_ids = data.get('record_ids', [])
    username = data.get('username', '')
    if not record_ids or username != uname:
        return
    record_ids = list(set(record_ids))
    operation_desc = mysql_op.delete_rows_from_data_center(record_ids, username, name)
    if not operation_desc.endswith("错误"):
        socketio.emit('s2c_delete_rows_from_data_center', {
            "record_ids": record_ids,
            "operation_desc": operation_desc
        })
    else:
        socketio.emit('s2c_operation_desc', operation_desc)
    # print("*" * 20)


# 可以使用同一个函数处理不同的事件
# @socketio.on('c2s_refresh_table_from_data_center', namespace='/a')
@socketio.on('c2s_refresh_table_from_data_center', namespace='/')
@login_require
def handle_refresh_table_from_data_center(uname, name):
    # 同步表格
    socketio.emit('s2c_init_table_data',
                  mysql_op.get_table_from_data_center(),
                  to=request.sid)
    # 同步今天操作日志
    today = time.strftime("%Y-%m-%d", time.localtime())
    socketio.emit('s2c_all_operation_logs_from_date', mysql_op.get_all_operation_logs_from_date(today),
                  to=request.sid)
    # socketio也可以和和http一样响应式回调callback
    # 返回数据即可
    return {"msg": "数据同步成功！", "type": "success"}
    # print("*" * 20)


@socketio.on("c2s_add_rows_to_data_center")
@login_require
def handle_add_rows(uname, name, data):
    # 判断该token是否有权限添加can_add
    auth = request.headers.get('Authorization', '')
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        privilege = redis_op.hget(auth, "can_add")
    if privilege is None or privilege == '×':
        return

    username = data.get('username', '')
    if username != uname:
        return
    fields = data.get('fields', [])
    rows = data.get('data', [])
    if not fields or not rows:
        return
    operation_desc = mysql_op.add_rows(fields, rows, username, name)
    if not operation_desc.endswith("错误"):
        socketio.emit('s2c_add_rows_to_data_center', {
            "data": mysql_op.get_table_from_data_center(),
            "operation_desc": operation_desc
        })
    else:
        socketio.emit('s2c_operation_desc', operation_desc)
    # print("*" * 20)


@socketio.on("c2s_update_data_center")
@login_require
def handle_update_data_center(uname, name, data):
    # print("c2s_update_data_center")
    field = data.get('field', '')
    # 判断该token是否有权限修改该字段
    auth = request.headers.get('Authorization', '')
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        privilege = redis_op.hget(auth, field)
    if privilege is None or privilege == '×':
        return

    username = data.get('username', '')
    if username != uname:
        return
    record_id = data.get('record_id', 0)

    if not record_id or 'value' not in data:
        return
    value = data['value']
    operation_desc = mysql_op.update_data_center(record_id, field, value, username, name)
    if not operation_desc.endswith("错误"):
        socketio.emit('s2c_update_data_center', {
            "record_id": record_id,
            "field": field,
            "value": value,
            "operation_desc": operation_desc
        })
    else:
        socketio.emit('s2c_operation_desc', operation_desc)

    # print("*" * 20)
