# coding:utf8
from .. import db
from .tags import post_tag_rela


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    article = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=post_tag_rela, lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title
