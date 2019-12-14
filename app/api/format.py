# coding:utf8
from flask import jsonify


class Format(object):
    """格式化响应内容"""

    @staticmethod
    def success(message='success', code=200, data=None):
        """操作成功

        Params:
            message (:obj:`str`, optional): 返回信息
            code (:obj:`int`, optional): 状态码
            data (:obj:`dict`, optional): 返回数据
        """
        if not isinstance(message, str):
            raise TypeError('message type must be a str')

        if not isinstance(code, int):
            raise TypeError('code type must be a number')

        if data and not isinstance(data, dict):
            raise TypeError('data type must be a dict')

        return jsonify(
            dict(
                status='success',
                message=message,
                code=code,
                data=data,
            )
        )

    @staticmethod
    def error(message='error', code=500):
        """操作失败

        Params:
            message (:obj:`str`, optional): 返回信息
            code (:obj:`int`, optional): 状态码
        """
        if not isinstance(message, str):
            raise TypeError('message type must be a str')

        if not isinstance(code, int):
            raise TypeError('code type must be a number')

        return jsonify(
            dict(
                status='error',
                message=message,
                code=code,
                data=None,
            )
        )
