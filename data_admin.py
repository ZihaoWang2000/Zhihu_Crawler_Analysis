# -*- coding:utf-8 -*-
import pymysql

# ******************************************数据库操作***************************************************#
class Database:
    # 数据库初始化，port得是数值int型,暂时先这样，（后续情况需要可以开放多库多服务器查询（允许传入参数）
    def __init__(self, ):
        self.host = '127.0.0.1'  # 主机名，默认本地
        # self.host = '101.201.198.35'  # 主机名，为服务器ip
        self.port = 3306  # 端口默认3306
        self.user = 'root'  # 用户名，默认root
        self.password = 'xxx'  # 密码
        # self.password = 'STourism@whu'  # 服务器密码
        self.db = 'zhihu'  # 数据库名
        self.charset = 'utf8'  # 数据库字符集，默认utf-8,7.31 xts,修改为utf8mb4，支持存储表情

    # **********************************数据库连接并执行的相关函数*********************************************#2.12更新可以批量插入和查询一个
    def database(self, sql, fetch='all', data_list='one'):
        o_type = sql.split(' ')[0].lower()
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)  # 连接数据库
        cur = conn.cursor()  # 用于访问和操作数据库中的数据（一个游标，像一个指针）
        if o_type == 'select':
            cur.execute(sql)  # 执行操作
            if fetch == 'all':
                result = cur.fetchall()  # 匹配所有满足的
            else:
                result = cur.fetchone()  # 匹配一个满足的
            cur.close()  # 关闭游标
            conn.close()  # 关闭数据库连接
            return result
        elif o_type == 'insert' or o_type == 'update' or o_type == 'delete':
            if data_list == 'one':
                try:
                    cur.execute(sql)
                    conn.commit()  # 提交事务
                    # print("{} ok".format(type))
                except Exception as e:  # 发生错误时回滚
                    print(e)
                    conn.rollback()  # 回滚事务
            else:  # 一次插入多条数据
                try:
                    cur.executemany(sql, data_list)  # 列表里面的单个数据必须是元组
                    conn.commit()  # 提交事务
                    # print("{} ok".format(type))
                except Exception as e:  # 发生错误时回滚
                    print(e)
                    conn.rollback()  # 回滚事务
            cur.close()  # 关闭游标
            conn.close()  # 关闭数据库连接


if __name__ == '__main__':
    Data_admin = Database()