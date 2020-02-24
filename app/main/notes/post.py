# coding:utf8
from . import notes
from flask import render_template, g, request, redirect, url_for
from app.auth.authentications import auth
from app.models import User, Post


@notes.route('/', methods=['GET'])
@auth.login_required
def posts():
    posts = g.current_user.posts
    return render_template('posts.html', posts=posts)
