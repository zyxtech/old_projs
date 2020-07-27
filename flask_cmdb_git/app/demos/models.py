# encoding: utf-8
from datetime import datetime

from .. import db


class DemoUser(db.Model):
    __tablename__ = 'DemoUser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    #username = db.Column(db.String(64), unique=True, index=True)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class DemoPost(db.Model):
    __tablename__ = 'DemoPost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('DemoUser.id'),
        nullable=False)

#    def __repr__(self):
#        return '<Post %r>' % self.title



