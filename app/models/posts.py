# coding:utf8
from .. import db
from .tags import post_tag_rela
from .users import User


class Post(db.Model):
    __tablename__ = 'TB_POSTS'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    article = db.Column(db.Text)
    users = db.Column(db.Integer, db.ForeignKey('TB_USERS.id'))
    tags = db.relationship('Tag', secondary=post_tag_rela, lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title
