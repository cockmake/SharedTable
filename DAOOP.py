from mysql.connector.pooling import MySQLConnectionPool

from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_POOL_SIZE
from utils import get_operation_description, get_update_operation_description


class MYSQLOP:
    def __init__(self):
        dbconfig = {
            "pool_name": f"{MYSQL_DATABASE}_pool",
            "pool_reset_session": True,
            "pool_size": MYSQL_POOL_SIZE,  # 最大连接数比最大可工作线程数多1
            "host": MYSQL_HOST,
            "user": MYSQL_USER,
            "password": MYSQL_PASSWORD,
            "port": MYSQL_PORT,
            "database": MYSQL_DATABASE
        }
        self.mysql_pool = MySQLConnectionPool(**dbconfig)
        self.user_table = "user_table"  # 已经注册的用户表
        self.user_to_register_table = "user_to_register_table"  # 待审核的用户表
        self.data_center_table = "data_center_table"  # 数据中心表
        self.operation_log_table = "operation_log_table"  # 操作日志表
        self.data_drop_table = "data_drop_table"  # 数据删除表
        # 用户可以修改的字段、允许插入、删除的表
        self.user_fields_table = "user_fields_table"  # 用户可以修改的字段表 （还包括增、删两个权限）

    def get_users_privilege(self):
        # 获取用户可以修改的字段
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM %s" % self.user_fields_table
                cursor.execute(sql)
                result = cursor.fetchall()
        return result
    def get_user_privilege(self, username, name):
        # 获取用户权限
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s' AND name = '%s'" % (self.user_fields_table, username, name)
                cursor.execute(sql)
                result = cursor.fetchone()
        return result
    def update_user_privilege(self, username, name, new_privilege):
        # new_privilege是一个字典key是字段名，value是权限
        # 更新用户权限
        sql = "UPDATE %s SET " % self.user_fields_table
        for key in new_privilege:
            sql += f"{key} = '{new_privilege[key]}', "
        sql = sql[:-2]
        sql += f" WHERE username = '{username}' AND name = '{name}'"
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def update_user_password_from_email(self, email, password):
        # 更新用户密码
        sql = "UPDATE %s SET password = '%s' WHERE email = '%s'" % (self.user_table, password, email)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def query_user_info_from_email(self, email):
        # 根据邮箱查询用户信息
        # 如果存在返回用户信息
        # 如果不存在返回None
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM %s WHERE email = '%s'" % (self.user_table, email)
                cursor.execute(sql)
                result = cursor.fetchone()
                return result

    def query_user_info_from_username(self, username):
        # 根据用户名查询用户信息
        # 如果存在返回用户信息
        # 如果不存在返回None
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s'" % (self.user_table, username)
                cursor.execute(sql)
                result = cursor.fetchone()
                return result

    def query_user_from_username(self, username):
        # 在两个表中查询是否存在该用户名
        # 如果存在返回True
        # 如果不存在返回False
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s'" % (self.user_table, username)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return True
                else:
                    sql = "SELECT * FROM %s WHERE username = '%s'" % (self.user_to_register_table, username)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if result:
                        return True
                    else:
                        return False

    def query_user_from_email(self, email):
        # 在两个表中查询是否存在该邮箱
        # 如果存在返回True
        # 如果不存在返回False
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM %s WHERE email = '%s'" % (self.user_table, email)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return True
                else:
                    sql = "SELECT * FROM %s WHERE email = '%s'" % (self.user_to_register_table, email)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if result:
                        return True
                    else:
                        return False

    def register_user_to_check(self, username, password, email, name, phone, operation_type="普通"):
        # 将用户注册信息插入待审核表
        sql = "INSERT INTO %s (username, password, email, name, phone, operation_type) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
            self.user_to_register_table, username, password, email, name, phone, operation_type)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_users_to_register(self):
        # 获取所有待审核用户
        sql = "SELECT username, email, name, operation_type, phone, request_time FROM %s" % self.user_to_register_table
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        for item in result:
            item['request_time'] = item['request_time'].strftime("%Y-%m-%d %H:%M:%S")
        return result

    def accept_register(self, username, email, name, phone):
        # 审核通过
        # 根据条件找到待审核用户
        # 将待审核用户插入已注册用户表
        # 删除待审核用户
        # 插入权限表
        sql_query = "SELECT * FROM %s WHERE username = '%s' AND email = '%s' AND name = '%s' AND phone = '%s'" % (
            self.user_to_register_table, username, email, name, phone)
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchone()
        if not result:
            return False
        password = result['password']
        operation_type = result['operation_type']
        sql_insert = "INSERT INTO %s (username, password, email, name, phone, operation_type) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
            self.user_table, username, password, email, name, phone, operation_type)
        sql_delete = "DELETE FROM %s WHERE username = '%s'" % (self.user_to_register_table, username)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 插入
                    cursor.execute(sql_insert)
                    # 删除
                    cursor.execute(sql_delete)
                    # 插入权限表
                    sql = "INSERT INTO %s (username, name) VALUES ('%s', '%s')" % (self.user_fields_table, username, name)
                    cursor.execute(sql)
                    # 提交
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def reject_register(self, username, email, name, phone):
        # 审核不通过
        # 删除待审核用户
        sql_delete = "DELETE FROM %s WHERE username = '%s' AND email = '%s' AND name = '%s' AND phone = '%s'" % (
            self.user_to_register_table, username, email, name, phone)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_delete)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_table_from_data_center(self):
        # 获取数据中心表
        # 其中的日期格式化为%Y-%m-%d
        sql = "SELECT * FROM %s" % self.data_center_table
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        for item in result:
            item['rq'] = item['rq'].strftime("%Y-%m-%d")
        return result

    def add_one_row_to_data_center(self, add_info, username, name):
        # 添加一行到数据中心表和操作日志表
        # 并获取改行插入的id id是自增的
        try:
            keys = list(add_info.keys())
            sql = "INSERT INTO %s (" % self.data_center_table
            sql += ", ".join(keys)
            sql += ") VALUES ("
            for key in keys:
                sql += "'%s', " % add_info[key]
            sql = sql[:-2]
            sql += ")"
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    last_id = cursor.lastrowid
                    add_info['record_id'] = last_id
                    operation_desc = get_operation_description(name, "增", last_id)
                    # 插入操作日志表
                    sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '增', '%s')" % (
                        self.operation_log_table, username, operation_desc)
                    cursor.execute(sql)
                    conn.commit()
            return add_info, operation_desc
        except Exception as e:
            print(e)
            return False, f"{name}执行操作时出现错误"

    def add_rows(self, fields, rows, username, name):
        # 添加多行到数据中心表
        # 并插入操作日志表
        try:
            sql = "INSERT INTO %s (" % self.data_center_table
            sql += ", ".join(fields)
            sql += ") VALUES "
            for row in rows:
                sql += "("
                for item in row:
                    sql += "'%s', " % item
                sql = sql[:-2]
                sql += "), "
            sql = sql[:-2]
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    last_id = cursor.lastrowid
                    operation_desc = get_operation_description(name, "批量增", [last_id, last_id + len(rows) - 1])
                    # 插入操作日志表
                    sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '增', '%s')" % (
                        self.operation_log_table, username, operation_desc)
                    cursor.execute(sql)
                    conn.commit()
            return operation_desc
        except Exception as e:
            print(e)
            return f"{name}执行操作时出现错误"

    def delete_rows_from_data_center(self, record_ids, username, name):
        # 数据删除表的结构和数据中心表一样
        # 将要删除的数据插入数据删除表（可以查询式插入）
        # 删除数据中心表中的多行
        # 并插入操作日志表
        if isinstance(record_ids, int):
            record_ids = [record_ids]
        try:
            sql_insert = "INSERT INTO %s SELECT * FROM %s WHERE record_id IN (" % (
            self.data_drop_table, self.data_center_table)
            for record_id in record_ids:
                sql_insert += "%s, " % record_id
            sql_insert = sql_insert[:-2]
            sql_insert += ")"
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 插入数据删除表
                    cursor.execute(sql_insert)
                    sql_delete = "DELETE FROM %s WHERE record_id IN (" % self.data_center_table
                    for record_id in record_ids:
                        sql_delete += "%s, " % record_id
                    sql_delete = sql_delete[:-2]
                    sql_delete += ")"
                    # 删除数据中心表
                    cursor.execute(sql_delete)
                    operation_desc = get_operation_description(name, "删", record_ids)
                    # 插入操作日志表
                    sql_insert = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '删', '%s')" % (
                        self.operation_log_table, username, operation_desc)
                    cursor.execute(sql_insert)
                    conn.commit()
            return operation_desc
        except Exception as e:
            print(e)
            return f"{name}执行操作时出现错误"

    def update_data_center(self, record_id, field, value, username, name):
        # 先查询原来field对应的数据便于生成操作描述
        # 更新数据中心表
        # 插入操作日志表
        try:
            sql_query = "SELECT %s FROM %s WHERE record_id = %s" % (field, self.data_center_table, record_id)
            print(sql_query)
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_query)
                    src_data = cursor.fetchone()[0]
                    sql_update = "UPDATE %s SET %s = '%s' WHERE record_id = %s" % (
                        self.data_center_table, field, value, record_id)
                    cursor.execute(sql_update)
                    operation_desc = get_update_operation_description(name, record_id, field, src_data, value)
                    # 插入操作日志表
                    sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '改', '%s')" % (
                        self.operation_log_table, username, operation_desc)
                    cursor.execute(sql)
                    conn.commit()
            return operation_desc
        except Exception as e:
            print(e)
            return f"{name}执行操作时出现错误"

    def write_operation_log(self, username, operation_type, operation_desc):
        # 插入操作日志表
        sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '%s', '%s')" % (
            self.operation_log_table, username, operation_type, operation_desc)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def get_all_operation_logs_from_date(self, today):
        # 获取当天所有操作日志的描述即可
        sql = "SELECT operation_desc FROM %s WHERE operation_time LIKE '%s%%'" % (self.operation_log_table, today)
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        return result
    def get_all_drop_data(self):
        # 获取所有删除的数据
        sql = "SELECT * FROM %s" % self.data_drop_table
        with self.mysql_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        for item in result:
            item['rq'] = item['rq'].strftime("%Y-%m-%d")
        return result
    def restore_drop_data(self, record_id, rq, sj, ch):
        # rq, sj, ch也需要做判断
        # 恢复删除的数据（表结构一样采用查询式插入）
        # 从数据删除表中删除

        sql_insert = "INSERT INTO %s SELECT * FROM %s WHERE record_id = %s AND rq = '%s' AND sj = '%s' AND ch = '%s'" % (
            self.data_center_table, self.data_drop_table, record_id, rq, sj, ch)
        sql_delete = "DELETE FROM %s WHERE record_id = %s AND rq = '%s' AND sj = '%s' AND ch = '%s'" % (
            self.data_drop_table, record_id, rq, sj, ch)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 插入数据中心表
                    cursor.execute(sql_insert)
                    # 删除数据删除表
                    cursor.execute(sql_delete)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_user(self, username, name):
        # 删除用户表中的用户
        # 删除用户权限表中的用户
        sql_delete_user = "DELETE FROM %s WHERE username = '%s' AND name = '%s'" % (self.user_table, username, name)
        sql_delete_privilege = "DELETE FROM %s WHERE username = '%s'" % (self.user_fields_table, username)
        try:
            with self.mysql_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_delete_user)
                    cursor.execute(sql_delete_privilege)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

