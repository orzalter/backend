# codng:utf8
from flask import Blueprint
from flask_restful import Api

auth = Blueprint('auth', __name__)
resource = Api(auth)

from . import authentications, errors