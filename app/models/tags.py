# coding:utf8
from .. import db


post_tag_rela = db.Table('TB_REL',
                         db.Column('tag_id', db.Integer,
                                   db.ForeignKey('TB_TAGS.id')),
                         db.Column('post_id', db.Integer,
                                   db.ForeignKey('TB_POSTS.id'))
                         )


class Tag(db.Model):
    __tablename__ = 'TB_TAGS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', secondary=post_tag_rela, lazy='dynamic')

    def __repr__(self):
        return '<Tag %r>' % self.name
