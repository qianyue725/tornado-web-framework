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


class AsyncHttpService:
    logger = logging.getLogger(__name__)

    @tornado.gen.coroutine
    def async_http_execute(self, url):
        resp = yield AsyncHTTPClient().fetch(url)
        self.logger.debug("client fetch result, code={}, message={}".format(resp.code, resp.body))
        if resp.code == 200:
            body = {"message": "client fetch success"}
        else:
            body = {"message": "client fetch error"}
        return body
