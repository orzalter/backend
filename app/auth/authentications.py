# coding:utf8
from flask import current_app, g, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app import redis
from app.models import User

from ..api import Format
from . import resource

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    try:
        if not username_or_token:
            return False
        if not password:
            # token
            g.current_user = User.verify_auth_token(username_or_token)
            g.token_used = True
            if g.current_user:
                token_id = 'Token-User-ID-' + str(g.current_user.id)
                token = redis.get(token_id)
                if token and token.decode('utf-8') == username_or_token:
                    return True
                return False

        user = User.query.filter_by(name=username_or_token).first()
        if not user:
            return False
        g.current_user = user
        g.token_used = True
        if user.verify_auth_password(password):
            return True
        return False
    except:
        return False


@resource.resource('/token')
class Auth(Resource):
    """ 登录验证 """

    decorators = [auth.login_required]

    def __init__(self):
        self.token_id = 'Token-User-ID-' + str(g.current_user.id)

    def get(self):
        """ 获取/生成token """
        token = redis.get(self.token_id)
        if token:
            return jsonify({'token': token.decode('utf-8'), 'expiration': redis.ttl(self.token_id)})
        else:
            token = g.current_user.generate_auth_token(
                expiration=current_app.config['TOKEN_EXPIRATION'])
            redis.set(self.token_id, token)
            redis.expire(self.token_id, current_app.config['TOKEN_EXPIRATION'])
            return jsonify({
                'token': token,
                'expiration': current_app.config['TOKEN_EXPIRATION']
            })
