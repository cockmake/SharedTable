import time

import redis
from flask import Blueprint, request

from celery_task import celery_send_email
from persistence import mysql_op, redis_pool
from request_wrap import request_fields_require, login_require
from utils.common import check_email_valid, generate_yzm, check_username_valid, check_password_valid, \
    generate_token, get_operation_description

user = Blueprint('user', __name__, url_prefix='/user')


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
    # print("注销成功！")
    return {"msg": "注销成功！", "type": "success"}
