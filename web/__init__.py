# -*- coding: utf-8 -*- #
"""
    __init__.py.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/8 下午2:14
"""
import logging
import os
import sys
import logging.handlers

import tornado.web

from .common import session
from .handlers import IndexHandler, TestCookieHandler, LoginHandler, UserHandler, AsyncRequestHandler


def init_logging(base_path=None):
    root_logger = logging.getLogger()
    logging_format = logging.Formatter(
        fmt='%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] - %(message)s'
    )

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setLevel(logging.DEBUG)
    std_handler.setFormatter(logging_format)

    log_path = os.path.join(base_path, 'logs/application.log')
    file_handler = logging.handlers.TimedRotatingFileHandler(log_path, when='MIDNIGHT', interval=1, backupCount=5,
                                                             encoding='UTF-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging_format)

    root_logger.addHandler(std_handler)
    root_logger.addHandler(file_handler)


class Application(tornado.web.Application):
    handlers = [
        (r'/index', IndexHandler),
        (r'/cookie', TestCookieHandler),
        (r'/login', LoginHandler),
        (r'/user/.*', UserHandler),
        (r'/async/.*', AsyncRequestHandler)
    ]
    settings = dict(
        # -------一般设置--------
        debug=True,
        compress_response=True,  # 如果设置 True, responses（响应）将被自动压缩
        # -------模板设置-------
        template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
        compiled_template_cache=True,
        autoescape=None,
        # -------认证安全设置-------
        # cookie标识位，用来给cookie签名。
        cookie_secret='LvTUiGEZEeqsxQAMKSw6LS701fBhGRHqrMUADCksOi0=',
        # 如果true, 跨站请求伪造(防护) 将被开启.
        xsrf_cookies=False,
        # -------静态文件设置-------
        static_hash_cache=False,
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        static_url_prefix='/static/',

        # ------session配置-------
        session_prefix_key='tornado-session-',
        session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
        session_timeout=60,
        store_options={
            'redis_host': '172.28.84.113',
            'redis_port': 6379
        },
    )

    def __init__(self):
        super(Application, self).__init__(
            handlers=self.handlers,
            **self.settings
        )
        self.session_manager = session.SessionManager(self.settings["session_secret"], self.settings["store_options"],
                                                      self.settings['session_prefix_key'],
                                                      self.settings["session_timeout"])
