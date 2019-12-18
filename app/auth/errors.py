# coding:utf8
from .authentications import auth

from ..api import Format


@auth.error_handler
def auth_error():
    return Format.error(message='auth error', code=401)
