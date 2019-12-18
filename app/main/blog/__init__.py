# coding:utf8
from flask import Blueprint
from flask_restful import Api

blog = Blueprint('blog', __name__)
resource = Api(blog)

from . import post, user