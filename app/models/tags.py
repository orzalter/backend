# coding:utf8
from .. import db


post_tag_rela = db.Table('post_tag_rela',
                         db.Column('tag_id', db.Integer,
                                   db.ForeignKey('tags.id')),
                         db.Column('post_id', db.Integer,
                                   db.ForeignKey('posts.id'))
                         )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', secondary=post_tag_rela, lazy='dynamic')

    def __repr__(self):
        return '<Tag %r>' % self.name
