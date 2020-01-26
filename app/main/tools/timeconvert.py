# coding:utf8
import datetime

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.api import Format

from . import resource


@resource.resource('/timeconvert')
class TimeConvert(Resource):
    """ 时间戳转时间格式 %Y-%m-%d %H:%M:%S"""

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument(
            'timestamp', location='json', type=int, required=True, help='timestamp')
        args = self.parser.parse_args()
        time_array = datetime.datetime.fromtimestamp(args['timestamp'])
        time_str = time_array.strftime("%Y-%m-%d %H:%M:%S")
        data = dict()
        data['datetime'] = time_str
        return Format.success(data=data)
