# -*- coding: utf-8 -*- #
"""
    __init__.py.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/8 下午4:58
"""
import logging
from datetime import datetime

import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient

from web.common import session
from web.common.commons import BaseDataResultGenerator
from web.common.exceptions import BusinessException, BussinessExceptionEnum
from web.mapper.mappers import UserMapper
from web.service.services import AsyncHttpService

LOGGER = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = session.Session(self.application.session_manager, self)
        if 'If-None-Match' in self.request.headers.keys():
            del self.request.headers['If-None-Match']

    def get_current_user(self):
        return self.session.get("user_name")

    def write_error(self, status_code: int, **kwargs) -> None:
        exception_instance = kwargs.get('exc_info')[1]
        result = None
        if isinstance(exception_instance, BusinessException):
            result = BaseDataResultGenerator.gen_fail_result(exception_instance.get_code(),
                                                             exception_instance.get_message())
        elif isinstance(exception_instance, NotImplementedError):
            result = BaseDataResultGenerator.gen_fail_result(500000, exception_instance.args[0])
        elif isinstance(exception_instance, Exception):
            result = BaseDataResultGenerator.gen_fail_result(400001, '未知错误.')
        self.finish(result)

    def _do_request(self, *args: str, **kwargs: str) -> None:
        self.service(*args, **kwargs)

    head = _do_request
    get = _do_request
    post = _do_request
    delete = _do_request
    patch = _do_request
    put = _do_request
    options = _do_request

    def service(self, *args, **kwargs):
        action = self.request.path.rsplit(r'/', maxsplit=1)[1]
        LOGGER.debug("action: {}".format(action))
        if not hasattr(self, action):
            raise NotImplementedError('{} Function NotImplemented'.format(action))
        getattr(self, action)(*args, **kwargs)


class LoginHandler(BaseHandler):
    def get(self):
        self.session["user_name"] = self.get_argument("user_name")
        self.session["age"] = 18
        self.session.save()
        self.write('save user_name to session')


class IndexHandler(BaseHandler):

    def get(self):
        title = self.get_argument('title', default='default_title')
        user_name = self.get_current_user()
        LOGGER.info('title: {}'.format(title))
        LOGGER.info('user_name: {}'.format(user_name))
        self.finish({
            'success': True,
            'server_time': int(datetime.now().timestamp()),
            'data': 'welcome to tornado server.'
        })


class TestCookieHandler(BaseHandler):

    def get(self):
        self.set_secure_cookie("user_name", "qianyue")
        self.finish("hello")


class UserHandler(BaseHandler):
    mapper = UserMapper()

    def list(self):
        data = self.mapper.get_all()
        result = BaseDataResultGenerator.gen_success_result(data=data)
        self.finish(result)

    def info(self):
        user_id = self.get_argument("user_id", None)
        if user_id is None:
            BussinessExceptionEnum.MISSING_REQUIRED_PARAMETER.throwException(message="缺少必要参数: {}".format("user_id"))
        data = self.mapper.get_user_info(user_id)
        result = BaseDataResultGenerator.gen_success_result(data=data)
        self.finish(result)

    def add(self):
        self.finish("post success.")


class AsyncRequestHandler(BaseHandler):

    # @tornado.web.asynchronous  ==>  使用tornado5.0.2
    @tornado.gen.coroutine
    def get(self):
        service = AsyncHttpService()
        body = yield service.async_http_execute("http://v.juhe.cn/fileconvert/query")
        self.finish(body)
