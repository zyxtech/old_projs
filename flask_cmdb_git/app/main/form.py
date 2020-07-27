# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, IPAddress

#ok
class User_Form(FlaskForm):
    id = HiddenField()
    user_name = StringField(u'姓名', validators=[Length(max=50)])
    nick_name = StringField(u'昵称', validators=[Length(max=50)])
    mobile = IntegerField(u'手机号')
    passwd = StringField(u'密码', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')



