# -*- coding: utf-8 -*- #
"""
    commons.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/10 下午1:34
"""
from datetime import datetime

from marshmallow import Schema, fields

from web.common.utils import ignore_null


class BaseDataResult:

    def __init__(self, error_code=None, error_message=None, success=True, data=None):
        self.data = data
        self.server_time = int(datetime.now().timestamp())
        self.error_code = error_code
        self.error_message = error_message
        self.success = success


class BaseDataResultSchema(Schema):
    data = fields.Field()
    error_code = fields.Integer()
    error_message = fields.Str()
    success = fields.Boolean()
    server_time = fields.Integer()


class BaseDataResultGenerator:
    schema = BaseDataResultSchema()

    @classmethod
    def gen_fail_result(cls, error_code, error_message) -> dict:
        result = BaseDataResult(error_code=error_code, error_message=error_message, success=False)
        return ignore_null(cls.schema.dump(result))

    @classmethod
    def gen_success_result(cls, data) -> dict:
        result = BaseDataResult(success=True, data=data)
        return ignore_null(cls.schema.dump(result))
