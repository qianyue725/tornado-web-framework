"""
    exceptions.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/10 下午5:44
"""
from enum import Enum


class BussinessExceptionEnum(Enum):
    def __init__(self, code, message):
        self.__code = code
        self.__message = message

    TIMEOUT_ERROR = (4000000, "请求超时")
    REQUEST_PARAMS_ERROR = (4000001, "错误的请求参数")
    MISSING_REQUIRED_PARAMETER = (4000005, "缺少必要参数")
    HTTP_REQUEST_FAIL = (500001, 'HTTP请求失败')

    def throwException(self, *, message: str = None) -> None:
        if message:
            self.__message = message  # 覆盖默认的错误提示
        raise BusinessException(self.__code, self.__message)


class BusinessException(Exception):
    '''业务异常类'''

    def __init__(self, code, message):
        self.__code = code
        self.__message = message

    def get_code(self):
        return self.__code

    def get_message(self):
        return self.__message
