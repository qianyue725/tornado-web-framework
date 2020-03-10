# -*- coding: utf-8 -*- #
"""
    database.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/9 上午11:35
"""
import pymysql
from DBUtils.PooledDB import PooledDB

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。
    ping=0,
    # ping MySQL服务端，检查是否服务可用。
    host='172.28.84.113',
    port=3306,
    user='root',
    password='root',
    database='test',
    charset='utf8mb4',
    autocommit=False,
    cursorclass=pymysql.cursors.DictCursor
)


class QueryRunner(object):

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def __prepare_connection(self):
        if self.connection_pool is None:
            raise SQLExcetion(
                "QueryRunner requires a connectionpool to be invoked in this way, or a Connection should be passed in")
        return self.connection_pool.connection()

    def fetch_all(self, sql, args=None):
        return self._query(sql, args, many=True)

    def fetch_one(self, sql, args=None):
        return self._query(sql, args)

    def _query(self, sql, args=None, many=False):
        conn = self.__prepare_connection()
        if conn is None:
            raise SQLExcetion("Null connection")
        if not sql or not isinstance(sql, str):
            raise SQLExcetion("Null SQL statement")
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, args)
            if many:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
        except Exception as e:
            raise SQLExcetion('sql execute failed. {}'.format(e.args))
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
        return result


class SQLExcetion(Exception):
    pass
