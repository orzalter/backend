# coding:utf8
from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
redis = FlaskRedis()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    redis.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main.blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    return app
