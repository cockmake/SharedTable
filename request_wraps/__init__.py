from functools import wraps

import redis
from flask import request

from persistence import redis_pool


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
