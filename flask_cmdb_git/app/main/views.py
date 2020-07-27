# -*- encoding:utf-8 -*-
"""
__author__=nieyabin
"""

import os
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import session, redirect, url_for, jsonify, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user

from . import main
from .. import db
from app.main.service import validator, service_user
from app.main.service.import_data import excel
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from app.main.models import User, UserForm
from app.main.form import User_Form

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@main.route('/', methods=['GET', 'POST'])
# @login_required
def index():
   
    return render_template('index.html')


@main.route('/reg_user')
def reg_user():

    data = dict()
    data['user_name'] = u'聂亚斌'
    data['nick_name'] = u'聂亚斌'
    data['mobile'] = u'18736064259'
    data['password'] = u'123456'
    data['email'] = u'123456@qq.com'
    ip = u'172.18.19.75'
    success, msg = service_user.create_user(data)

    return jsonify({"success":success, "msg":msg})


@main.route('/login', methods=['GET'])
def login():

    next_url = request.args.get("next", "/")
    flash("")
    return render_template("login.html", next=next_url, get_flashed_messages=get_flashed_messages)


@main.route('/login/user', methods=['GET', 'POST'])
def login_with_user():
    username = request.form.get("username")
    password = request.form.get("password")
    next_url = request.form.get("next")
    remember = request.form.get("remember", "no")
    rv = validator.validate_login_user(username.strip())
    if rv == "email":
        user = service_user.get_user_by_email(username.strip())
        print "===email====", user
        success, msg = validator.validate_login_password(user, password)
    elif rv == "mobile":
        user = service_user.get_user_by_mobile(username.strip())
        print "===mobile===", user
        success, msg = validator.validate_login_password(user, password)
    else:
        flash(u"您输入的用户名称或者密码有误!")
        return redirect(url_for('.login'))

    if not success:
        flash(msg)
        return redirect(url_for('.login'))

    if remember == 'no':
        login_user(user)
    else:
        login_user(user, remember=True)
    return redirect(next_url)


@main.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/")


@main.route('/users/manage')
def users_manage():
    listnames = [u"id", u"姓名", u"昵称", u"手机号" , u"操作"]
    return render_template('users_manage.html', listnames=listnames, formurl="/users/user_form",
                           name=u"user列表",
                           ajaxl="/users/users_list")


@main.route('/users/users_list')
def users_list():
    ajaxresult = []
    for ser in User.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.user_name)
        ajaxlist.append(ser.nick_name)
        ajaxlist.append(ser.mobile)
        ajaxresult.append(ajaxlist)
    print ajaxresult

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@main.route('/users/user_form', methods=['GET', 'POST'])
@login_required
def user_form():
    id = 0
    if request.args.has_key('id') or request.args.get('set'):
        id = request.args.get('id', 0, type=int)
        if not id:
            id = current_user.id
        user = User.query.filter_by(id=id).first()
    else:
        user = User()
    form = User_Form(obj=user)
    if form.validate_on_submit():
        user.user_name = form.user_name.data
        user.nick_name = form.nick_name.data
        user.mobile = form.mobile.data
        if id not in [0, '']:
            if not form.passwd.data =='':
                user.passwd = form.passwd.data
            db.session.add(user)
        else:
            user_exits = User.query.filter_by(mobile=form.mobile.data).first()
            if user_exits:
                flash(u'用户手机号已存在')
                return render_template('normal_form.html', form=form, name=u"用户",
                                       get_flashed_messages=get_flashed_messages)
            elif form.passwd.data in [u'', '', None, 0]:
                flash(u'密码格式不正确')
                return render_template('normal_form.html', form=form, name=u"用户", get_flashed_messages=get_flashed_messages)
            user.passwd = form.passwd.data

            # form.populate_obj(user)
            db.session.add(user)
        db.session.commit()
        return redirect(url_for('.users_manage'))
    return render_template('normal_form.html', form=form, name=u"用户", get_flashed_messages=get_flashed_messages)


@main.route('/users/user_form_del', methods=['GET', 'POST'])
def user_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            User.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)



# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session
#
#
# class DemoUser2Form(ModelForm):
#     class Meta:
#         model = DemoUser
#     submit = SubmitField(u'提交')





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/import/data', methods=['GET', 'POST'])
def import_data():
    # msg = excel("/home/nieyb/222.xls")
    #
    # return jsonify(msg)
    if request.method == 'POST':
        file = request.files['file']
        if not allowed_file(file.filename):
            flash(u"导入文件有误!")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # return render_template('im')
    return render_template('import_data.html', get_flashed_messages=get_flashed_messages)


@main.route('/test/current_user')
def test_current_user():
    user = current_user

    return jsonify({'user':user.user_name})


@main.route('/tool/resetdb')
def resetdb():
    db.drop_all()
    db.create_all()

    return render_template('index.html')