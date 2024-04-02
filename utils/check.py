import inspect
import re


def get_func_param_number(func):
    signature = inspect.signature(func)
    params = signature.parameters
    keys = set(params.keys()) - {'args', 'kwargs'}
    return len(keys)


def check_username_valid(username):
    # 用户名长度为6-20个字符，只能包含字母、数字、下划线
    if len(username) < 6 or len(username) > 20:
        return False
    if re.search(r'[^a-zA-Z0-9_]', username):
        return False
    return True


def check_password_valid(password):
    # 密码长度为8-16个字符，只能包含字母、数字、下划线、特殊字符
    if len(password) < 8 or len(password) > 16:
        return False
    if re.search(r'[^a-zA-Z0-9_~!@#$%^&*()+`\-={}|\[\]:";\'<>?,./]', password):
        return False
    return True


def check_email_valid(email):
    # 检查邮箱格式是否正确
    if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return True
    else:
        return False


def check_phone_valid(phone, *args, **kwargs):
    # 手机号只允许输入数字且长度为11位
    if len(phone) != 11:
        return False
    if re.search(r'[^0-9]', phone):
        return False
    return True
