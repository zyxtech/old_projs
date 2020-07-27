# encoding: utf-8
from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from wtforms import StringField, SubmitField, TextField, HiddenField, SelectField


#class Role(db.Model):
#    __tablename__ = 'roles'
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(64), unique=True)
#    users = db.relationship('User', backref='role', lazy='dynamic')

    #def __repr__(self):
        #return '<Role %r>' % self.name


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#   #  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username


def db_save(dbs, bing=None):
    try:
        db.session.add(dbs)
        db.session.commit()
        return True
    except Exception as e:
        print e
        return False


def db_delete(dbs, bing=None):
    db.session.delete(dbs)
    db.session.commit()


def db_commit():
    db.session.commit()



class User(db.Model, UserMixin):
    """用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    nick_name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return '<user_name %r>' % self.user_name

    @property
    def passwd(self):
        raise AttributeError('password is not a readable attribute')

    @passwd.setter
    def passwd(self, passwd):
        self.password = generate_password_hash(str(passwd))

    def verify_password(self, passwd):
        return check_password_hash(self.password, str(passwd))

    # token 验证
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def verify_password_or_token(self, token, passwd):
        user = User.verify_auth_token(token)
        if user:
            return True
        return check_password_hash(self.password, str(passwd))

    @classmethod
    def get_session(self):
        return db.session


class UserForm(User):
    class Meta:
        model = User
    submit = SubmitField(u'提交')