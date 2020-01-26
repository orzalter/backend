# coding:utf8
from flask import Blueprint
from flask_restful import Api

tools = Blueprint('tools', __name__)
resource = Api(tools)

from . import timeconvert
