# -*- coding: utf-8 -*- #
"""
    server.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/8 下午2:13
"""
import os

import tornado.httpserver
import tornado.ioloop
import tornado.log
from tornado.options import define, options

from web import Application, init_logging

define(name='port', default=8012, type=int, help='The Server Runs on The Given Port')
define(name='host', default='0.0.0.0', type=str, help='The Server Runs on The Given Host')
BASE_PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    app = Application()
    init_logging(BASE_PATH)
    options.parse_command_line()  # 执行这个函数会更改logging的日志级别,根据--logging命令行参数,默认是info级别
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(port=options.port, address=options.host)
    tornado.ioloop.IOLoop.current().start()