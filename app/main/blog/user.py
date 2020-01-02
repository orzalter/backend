# coding:utf8
import json
from json.decoder import JSONDecodeError

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from app import db
from app.api.format import Format
from app.models import *
from app.auth.authentications import auth

from . import blog, resource


@resource.resource('/user')
class BlogUser(Resource):
    """用户操作"""

    decorators = [auth.login_required]

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """获取单个用户信息

        Params:
            id (:obj:`int`): id

        Returns:
            Post:
                id        (int):     id
                name      (str):     名称
                role_id   (id):      角色ID
                role_name (str):     角色名称
        """
        self.parser.add_argument(
            'id', location='args', type=int, required=True, help='id')
        args = self.parser.parse_args()

        data = dict()

        user = User.query.filter_by(id=args['id']).first()
        if not user:
            return Format.error(message='User (id) not exists', code=404)

        # 角色名称
        try:
            role_name = user.roles.name
        except:
            role_name = None

        data['user'] = dict(
            id=user.id,
            name=user.name,
            role_id=user.role_id,
            role_name=role_name,
        )

        return Format.success(data=data)

    def post(self):
        """新增或編輯用户信息

        Params:
            id (:obj:`int`): id

        Returns:
            User:
                id            (int):  id
                name          (str):  名称
                password      (str)： 密码
                role_name     (str):  角色名称
        """
        self.parser.add_argument(
            'id', location='json', type=int, help='id')
        self.parser.add_argument(
            'name', location='json', type=str, required=True, help='name')
        self.parser.add_argument(
            'password', location='json', type=str, required=True, help='password')
        self.parser.add_argument(
            'role_name', location='json', type=str, required=True, help='admin, writer, reader')
        args = self.parser.parse_args()

        if args['id']:
            #  編輯
            bloguser = User.query.filter_by(id=args['id']).first()
            if not bloguser:
                return Format.error(message='User infor error')
        else:
            if User.query.filter_by(name=args['name']).first():
                return Format.error(message='User exists')
            bloguser = User(name=args['name'])

        bloguser.name = args['name']
        bloguser.password = args['password']
        role = Role.query.filter_by(name=args['role_name']).first()
        if not role:
            return Format.error(message='invalid role name')
        bloguser.role_id = role.id
        try:
            data = dict()
            data['user'] = dict(name=args['name'])
            db.session.add(bloguser)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return Format.error(message='User commit error')
        return Format.success(data=data)

    def delete(self):
        """删除指定用户

        Params:
            id (:obj:`int`): 文章id
        """
        self.parser.add_argument(
            'id', location='args', type=int, required=True, help='id')
        args = self.parser.parse_args()

        user = User.query.filter_by(id=args['id']).first()

        if not user:
            return Format.error(message='User (id) not exists')

        try:
            data = dict()
            data['user'] = dict(name=user.name)
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return Format.error(message='Delete user fail')
        return Format.success(data=data)
