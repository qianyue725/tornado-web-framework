# -*- coding: utf-8 -*- #
"""
    mappers.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/9 下午3:55
"""
import json
import logging

from web.database import QueryRunner, POOL


class UserMapper:
    query_runner = QueryRunner(POOL)
    logger = logging.getLogger(__name__)

    def get_all(self):
        result = None
        try:
            sql = 'select * from t_user_0'
            result = self.query_runner.fetch_all(sql)
            self.logger.debug('db return data: {}'.format(json.dumps(result)))
        except Exception as e:
            print(e)
        return result

    def get_user_info(self, id):
        result = None
        try:
            sql = 'select * from t_user_0 where id = %s'
            result = self.query_runner.fetch_one(sql, id)
            self.logger.debug('db return data: {}'.format(json.dumps(result)))
        except Exception as e:
            print(e)
        return result
