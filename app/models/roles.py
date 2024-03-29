# coding:utf8
from .. import db


class Role(db.Model):
    __tablename__ = 'TB_ROLES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='TB_ROLES', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
