# coding:utf8
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from config import config

cors = CORS()
db = SQLAlchemy()
redis = FlaskRedis()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    cors.init_app(app)
    db.init_app(app)
    redis.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main.tools import tools as tools_blueprint
    app.register_blueprint(tools_blueprint, url_prefix='/tools')

    from .main.blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    return app
