# -*- coding: utf-8 -*- #
"""
    tools.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/8 下午4:54
"""


def get_cookie_secret():
    from base64 import b64encode
    from uuid import uuid1
    print(b64encode(uuid1().bytes + uuid1().bytes))


def ignore_null(obj: dict):
    if not isinstance(obj, dict) or obj is None:
        return
    for key in list(obj.keys()):
        if obj[key] is None:
            obj.pop(key)
    return obj
