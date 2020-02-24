# coding:utf8
from flask import Blueprint
# from flask_restful import Api

notes = Blueprint('notes', __name__)
# resource = Api(notes)

from . import post