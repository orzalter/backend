# coding:utf8

import os


class Config(object):
    # WTF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'orzalter'
    # database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis expiration time
    TOKEN_EXPIRATION = os.environ.get('TOKEN_EXPIRATION') or 3600

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    pass


class TestConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0@127.0.0.1:3306/test"
    REDIS_URL = 'redis://:0@127.0.0.1:6379/0'
    # TESTING
    TESTING = True


class DevConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0@127.0.0.1:3306/web"
    REDIS_URL = 'redis://:0@127.0.0.1:6379/0'
    DEBUG = True


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
