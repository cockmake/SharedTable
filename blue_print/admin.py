from flask import Blueprint, request

from persistence.mysql_pool import mysql_op
from request_wrap import request_fields_require

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/all_users_to_register', methods=['GET'])
def admin_get_users_to_register():
    result = mysql_op.get_users_to_register()
    return result


@admin.route('/accept_register', methods=['POST'])
@request_fields_require('username', 'email', 'name', 'phone')
def admin_accept_register():
    data = request.json
    username = data['username']
    email = data['email']
    name = data['name']
    phone = data['phone']
    result = mysql_op.accept_register(username, email, name, phone)
    if result:
        return {"msg": "审核成功！", "type": "success"}
    return {"msg": "审核失败！", "type": "error"}


@admin.route('/all_drop_data', methods=['GET'])
def admin_get_all_drop_data():
    result = mysql_op.get_all_drop_data()
    return result


@admin.route('/restore_drop_data', methods=['POST'])
@request_fields_require('record_id')
def admin_restore_drop_data():
    data = request.json
    record_id = data['record_id']
    rq = data.get('rq', '')
    sj = data.get('sj', '')
    ch = data.get('ch', '')
    result = mysql_op.restore_drop_data(record_id, rq, sj, ch)
    if result:
        return {"msg": "恢复成功！", "type": "success"}
    return {"msg": "恢复失败！", "type": "error"}


@admin.route('/delete_user', methods=['POST'])
@request_fields_require('username', 'name')
def admin_delete_user():
    data = request.json
    username = data['username']
    name = data['name']
    result = mysql_op.delete_user(username, name)
    if result:
        return {"msg": "删除成功！", "type": "success"}
    else:
        return {"msg": "删除失败！", "type": "error"}


@admin.route('/reject_register', methods=['POST'])
@request_fields_require('username', 'email', 'name', 'phone')
def admin_reject_register():
    data = request.json
    username = data['username']
    email = data['email']
    name = data['name']
    phone = data['phone']
    result = mysql_op.reject_register(username, email, name, phone)
    if result:
        return {"msg": "删除成功！", "type": "warning"}
    else:
        return {"msg": "删除失败！", "type": "error"}


@admin.route('/get_users_privilege', methods=['GET'])
def user_get_users_privilege():
    result = mysql_op.get_users_privilege()
    return result


@admin.route('/update_user_privilege', methods=['POST'])
@request_fields_require('username', 'name', 'new_privilege')
def user_update_user_privilege():
    data = request.json
    username = data['username']
    name = data['name']
    new_privilege = data['new_privilege']
    result = mysql_op.update_user_privilege(username, name, new_privilege)
    if result:
        return {"msg": "修改成功！", "type": "success"}
    return {"msg": "修改失败！", "type": "error"}
