import random
import re
import smtplib
import string
import time
from email.header import Header
from email.mime.text import MIMEText

import jwt

from settings import SECRET_KEY, sender, mail_pass

key_convert = {
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


def generate_token(username, cur_t, alive_time, user_type='user'):
    # alive_time单位为秒
    # 使用jwt 根据secret_key生成token
    # token中包含用户名、当前时间戳和过期时间戳。
    encode_info = {
        'username': username,
        'login_time': cur_t,
        'expire_time': cur_t + alive_time,
        'user_type': user_type
    }
    encoded_jwt = jwt.encode(encode_info, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token):
    # 使用jwt解码token
    # 如果token过期或者token不正确，会抛出异常
    try:
        decode_info = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decode_info
    except Exception as e:
        return None


# 生成六位数字验证码
def generate_yzm(yzm_len=6):
    chars = string.digits
    return ''.join(random.choice(chars) for _ in range(yzm_len))


def send_email_to_user(user_email, subject, content):
    html_content = f"""
    <html>
        <body>
            <h1>{subject}</h1>
            <p>这是您的验证码：<b><font color='red' size='4'>{content}</font></b>。请在10分钟内完成您的操作，感谢您的使用。</p>
        </body>
    </html>
    """

    mail_host = "smtp.qq.com"  # 设置服务器
    message = MIMEText(html_content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = user_email
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(sender, mail_pass)
        smtpObj.sendmail(sender, [message['To']], message.as_string())
        smtpObj.close()
        return True
    except Exception as e:
        return False


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


def check_phone_valid(phone):
    # 手机号只允许输入数字且长度为11位
    if len(phone) != 11:
        return False
    if re.search(r'[^0-9]', phone):
        return False
    return True


def format_current_time():
    # 格式化当前时间
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_update_operation_description(username, affected_id, field_name, src_data, target_data):
    """
    根据操作类型和受影响的id列表生成操作描述
    :param username: str
    :param affected_id: int
    :param field_name: str
    :param src_data: str
    :param target_data: str
    :return: str
    """
    if field_name in key_convert:
        field_name = key_convert[field_name]
        return f"{format_current_time()}：\n用户{username}修改了\n序号为{affected_id}的{field_name}数据\n原数据为：{src_data}\n修改后的数据为：{target_data}".replace(
            '\'', '')
    else:
        print(field_name)
        return f"执行时发生错误"


def get_operation_description(username, operation_type, affected_ids):
    """
    根据操作类型和受影响的id列表生成操作描述
    :param username: str
    :param operation_type: 增、删、批量增、登录、注销
    :param affected_ids: type: list、int
    :return: str
    """
    if operation_type in ["增", "删"]:
        return f"{format_current_time()}：\n用户{username}{operation_type}了\n序号为：{affected_ids}的数据".replace('\'',
                                                                                                                  '')
    elif operation_type == "批量增":
        return f"{format_current_time()}：\n用户{username}批量增加了\n序号为：{affected_ids[0]} -- {affected_ids[1]}的数据".replace(
            '\'', '')
    elif operation_type == "登录":
        return f"{format_current_time()}：\n用户{username}登录了系统"
    elif operation_type == "注销":
        return f"{format_current_time()}：\n用户{username}退出了系统"
    else:
        return "未知操作类型"