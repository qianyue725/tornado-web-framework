# -*- coding: utf-8 -*- #
"""
    services.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/10 上午11:42
"""
import logging
import tornado.gen

from tornado.httpclient import AsyncHTTPClient

from web.common.commons import BaseDataResultGenerator
from web.common.exceptions import BussinessExceptionEnum


class AsyncHttpService:
    logger = logging.getLogger(__name__)

    @tornado.gen.coroutine
    def async_http_execute(self, url):
        result = None
        try:
            response = yield AsyncHTTPClient().fetch(url)
            self.logger.debug("client fetch result, code={}, message={}".format(response.code, response.body))
            if response.code == 200:
                result = BaseDataResultGenerator.gen_success_result(data=response.body.decode('utf-8'))
            else:
                result = BaseDataResultGenerator.gen_fail_result(600000, 'url: {},请求失败. error_code={}'.format(url, response.code))
        except Exception as e:
            self.logger.error("{} fetch fail, error_message={}".format(url, e.args))
            BussinessExceptionEnum.HTTP_REQUEST_FAIL.throwException()
        return result
