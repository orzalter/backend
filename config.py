# coding:utf8

import os


class Config(object):
    # WTF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'orzalter'
    # database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    pass


class TestConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0@127.0.0.1:3306/test"
    # TESTING
    TESTING = True


class DevConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0@127.0.0.1:3306/web"
    DEBUG = True


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
