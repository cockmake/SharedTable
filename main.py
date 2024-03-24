import time
from functools import wraps

import redis
from flask import Flask, request, Blueprint
from flask_cors import CORS
from flask_socketio import SocketIO

from DAOOP import MYSQLOP
from settings import REDIS_POOL_SIZE, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from utils import check_email_valid, generate_yzm, check_password_valid, check_username_valid, \
    generate_token, get_operation_description

from celery_task import celery_send_email

app = Flask(__name__)
CORS(app)

user = Blueprint('user', __name__, url_prefix='/user')
admin = Blueprint('admin', __name__, url_prefix='/admin')

# socketio配置
cors_allowed_origins = "*"
namespace = "/"
socketio = SocketIO(app, cors_allowed_origins=cors_allowed_origins, namespace=namespace)

mysql_op = MYSQLOP()

redis_config = {
    "max_connections": REDIS_POOL_SIZE,  # 最大连接数比最大可工作线程数多1
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_DB,
    "password": REDIS_PASSWORD,
    "decode_responses": True,
}
redis_pool = redis.ConnectionPool(**redis_config)


def login_require(f):
    # 在这里检查headers中的Authorization | access_token
    @wraps(f)  # wraps(f) 作用是获取原来函数的属性
    def inline_function(*args, **kwargs):
        # 原来f的里面的参数会传递到这里来
        access_token = request.headers.get('Authorization', '')
        if not access_token:
            return {'msg': 'access_token required', 'type': 'error'}, 401
        # 从redis中获取用户名
        with redis.Redis(connection_pool=redis_pool) as redis_op:
            username = redis_op.hget(access_token, "username")
            name = redis_op.hget(access_token, "name")
        if username is None:
            return {'msg': 'access_token error', 'type': 'error'}, 401
        # 回去继续执行f这里，传入username
        return f(username, name, *args, **kwargs)  # 这里可以重新设置参数

    return inline_function


def request_fields_require(*field_names):
    # 检查post的参数
    # 只简单的检查是否存在且不为空
    # 这个参数是自定义的装饰器参数 和 inline_function 中的参数不同
    # 如果需要参数残传递进来就必须再套这一层

    def decorator(f):
        @wraps(f)
        def inline_function(*args, **kwargs):
            # 原来f的里面的参数会传递到这里来
            if request.method == 'GET':
                keys_set = request.args.keys()
                info_dict = request.args
            elif request.method == 'POST':
                keys_set = request.json.keys()
                info_dict = request.json
            else:
                return {'msg': 'method not allowed', 'type': 'error'}, 405
            for field_name in field_names:
                if field_name not in keys_set:
                    return {'msg': f'{field_name} required', 'type': 'error'}, 400
                elif info_dict[field_name] == '' or info_dict[field_name] is None:
                    return {'msg': f'{field_name} can not be empty', 'type': 'error'}, 400

            # 回去继续执行f
            return f(*args, **kwargs)  # 这里可以重新设置参数

        return inline_function

    return decorator


@user.route('/register_yzm', methods=['POST'])
@request_fields_require('email')
def user_register_yzm():
    data = request.json
    email = data['email']
    if not check_email_valid(email):
        return {"msg": "错误的邮箱格式！", "type": "error"}
    # 查询数据库是否已经存在
    if mysql_op.query_user_from_email(email):
        return {"msg": "邮箱已经被注册或正在审核中！", "type": "error"}
    # 生成验证码
    yzm = generate_yzm()
    # 采用Celery异步发送
    celery_send_email.delay(email, '汽车租聘数据处理系统', yzm)
    # 同步发送邮件
    # send_result = send_email_to_user(email, '汽车租赁数据处理系统', yzm)
    # if not send_result:
    #     return {"msg": "邮件发送失败！", "type": "error"}
    # 保存验证码到redis
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        redis_op.set('register_' + email, yzm, ex=60 * 10)  # 10分钟过期
    return {"type": "success", "msg": "邮件发送成功！请核对验证邮箱，注意查收验证码。"}


@user.route('/find_password_yzm', methods=['POST'])
@request_fields_require('email')
def find_password_yzm():
    data = request.json
    email = data['email']
    if not check_email_valid(email):
        return {"msg": "错误的邮箱格式！", "type": "error"}
    # 查询数据库是否已经存在
    # 邮箱必须存在才能发送验证码
    result = mysql_op.query_user_info_from_email(email)
    if not result:
        return {"msg": "该邮箱没有注册记录！", "type": "error"}
    username = result['username']
    # 生成验证码
    yzm = generate_yzm()
    # 采用Celery异步发送
    celery_send_email.delay(email, '汽车租聘数据处理系统', yzm)
    # 同步发送邮件
    # send_result = send_email_to_user(email, '汽车租聘数据处理系统', yzm)
    # if not send_result:
    #     return {"msg": "邮件发送失败！", "type": "error"}
    # 保存验证码到redis
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        redis_op.set('find_password_' + email, yzm, ex=60 * 10)  # 10分钟过期
    return {"type": "success", "msg": f"邮件发送成功！您正在为 {username} 修改密码，注意查收验证码。",
            "username": username}


@user.route('/find_password', methods=['POST'])
@request_fields_require('email', 'password', 'yzm')
def find_password():
    data = request.json
    email = data['email']
    password = data['password']
    yzm = data['yzm']
    # 检查通过email检查用户是否存在
    user_info = mysql_op.query_user_info_from_email(email)
    if not user_info:
        return {"msg": "用户不存在！", "type": "error"}
    # 检查验证码是否正确
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        redis_yzm = redis_op.get('find_password_' + email)
    if yzm != redis_yzm:
        return {"msg": "请检查验证码和邮箱的正确性！", "type": "error"}
    # 修改密码
    result = mysql_op.update_user_password_from_email(email, password)
    if result:
        with redis.Redis(connection_pool=redis_pool) as redis_op:
            redis_op.delete('find_password_' + email)
        return {"msg": "密码修改成功！", "type": "success"}
    else:
        return {"msg": "密码修改失败！", "type": "error"}


@user.route('/register', methods=['POST'])
@request_fields_require('username', 'email', 'password', 'yzm', 'name', 'phone', 'operation_type')
def user_register():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    yzm = data['yzm']
    name = data['name']
    phone = data['phone']
    operation_type = data['operation_type']
    # 检查操作类型
    if operation_type not in ['管理员', '普通']:
        return {"msg": "操作类型错误！", "type": "error"}
    # 检查用户名是否符合要求
    if not check_username_valid(username):
        return {"msg": "用户名不符合要求！", "type": "error"}
    # 检查用户名是否存在
    if mysql_op.query_user_from_username(username):
        return {"msg": "用户名已经存在或正在审核中！", "type": "error"}
    # 检查密码
    if not check_password_valid(password):
        return {"msg": "用户名不符合要求！", "type": "error"}
    # 不要检查邮箱是否存在，因为注册验证码的检查需要邮箱存在
    # 检查验证码是否正确
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        redis_yzm = redis_op.get('register_' + email)
    if yzm != redis_yzm:
        return {"msg": "请检查验证码和邮箱的正确性！", "type": "error"}
    # 注册并删除验证码
    register_result = mysql_op.register_user_to_check(username, password, email, name, phone, operation_type)
    if register_result:
        with redis.Redis(connection_pool=redis_pool) as redis_op:
            redis_op.delete('register_' + email)
        return {"msg": "信息申请成功，请等待管理员审核！", "type": "success"}
    else:
        return {"msg": "注册失败！", "type": "error"}


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


@user.route('/login', methods=['POST'])
@request_fields_require('username', 'password')
def user_login():
    data = request.json
    username = data['username']
    password = data['password']
    user_info = mysql_op.query_user_info_from_username(username)
    if not user_info:
        return {"msg": "用户名不存在或在审核中！", "type": "error"}
    password_db = user_info['password']
    if password != password_db:
        return {"msg": "密码错误！", "type": "error"}
    user_type = user_info['operation_type']
    day_access = 3
    cur_t = int(time.time())
    time_to_live = day_access * 24 * 60 * 60
    token = generate_token(username, cur_t, time_to_live, user_type=user_type)
    name = user_info['name']
    # 把该用户的权限写入redis
    # 根据用户名查询权限
    privilege = mysql_op.get_user_privilege(username, name)  # privilege 是 dict 包含了username name 权限
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        # 以token为key 需要写入字段 用户名 姓名 *权限 操作类型
        # 最后设置过期时间
        redis_op.hset(token, mapping=privilege)
        redis_op.hset(token, "operation_type", user_type)
        redis_op.expire(token, time_to_live)
    # 写入登录日志
    login_desc = get_operation_description(name, "登录", [])
    # 将信息登录日志写入数据库
    mysql_op.write_operation_log(username, "登录", login_desc)
    return {"msg": "登录成功！", "type": "success", "access_token": token, "username": username,
            "name": name, "operation_type": user_type, 'privilege': privilege}


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


@user.route('/check_access_token', methods=['POST'])
@request_fields_require('access_token')
def user_check_access_token():
    data = request.json
    access_token = data['access_token']
    with redis.Redis(connection_pool=redis_pool) as redis_op:
        username = redis_op.get(access_token)
    if not username:
        return {"msg": "token无效！", "type": "error"}
    return {"msg": "token有效！", "type": "success", "username": username}


@user.route('/logout', methods=['GET'])
@login_require
def user_logout(username, name):
    access_token = request.headers['Authorization']

    if name:
        logout_desc = get_operation_description(name, "注销", [])
        mysql_op.write_operation_log(username, "注销", logout_desc)

    with redis.Redis(connection_pool=redis_pool) as redis_op:
        redis_op.delete(access_token)
    print("注销成功！")
    return {"msg": "注销成功！", "type": "success"}


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


@socketio.on('connect')
@login_require
def handle_connect(uname, name):
    print('客户端连接成功')

    socketio.emit('s2c_init_table_data',
                  mysql_op.get_table_from_data_center(),
                  to=request.sid)

    # 将登录信息发送除了自己以外的前端（因为下面会同步所有的操作日志，只有其他客户端需要这条信息）
    login_desc = get_operation_description(name, "登录", [])
    socketio.emit('s2c_operation_desc', login_desc, include_self=False)
    # 自己同步今天所有的操作日志
    today = time.strftime("%Y-%m-%d", time.localtime())
    socketio.emit('s2c_all_operation_logs_from_date', mysql_op.get_all_operation_logs_from_date(today),
                  to=request.sid)
    print("*" * 20)


@socketio.on('disconnect')
def handle_disconnect():
    print('客户端断开连接')
    print("*" * 20)


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
    print("*" * 20)


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
    print("*" * 20)


@socketio.on('c2s_refresh_table_from_data_center')
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
    print("*" * 20)


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
    print("*" * 20)


@socketio.on("c2s_update_data_center")
@login_require
def handle_update_data_center(uname, name, data):
    print("c2s_update_data_center")
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

    print("*" * 20)


app.register_blueprint(user)
app.register_blueprint(admin)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
