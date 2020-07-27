# encoding: utf-8
# -*- coding: utf-8 -*-
# coding:utf-8

from flask import render_template, redirect, url_for, request, jsonify, session
from flask_wtf import FlaskForm, RecaptchaField, Form
from wtforms import StringField, SubmitField, TextField, HiddenField, SelectField
from wtforms.validators import DataRequired, InputRequired, IPAddress, ValidationError, Length
from wtforms_alchemy import model_form_factory, QuerySelectField
import datetime

from app import db
from .models import DemoUser, DemoPost
from . import demos


@demos.route('/demos/index', methods=['GET', 'POST'])
@demos.route('/demos/', methods=['GET', 'POST'])
def index():
    return render_template('demos/index.html')


@demos.route('/demos/datatables', methods=['GET', 'POST'])
def datatables():
    return render_template('demos/datatables.html')


@demos.route('/demos/ajax_add_numbers')
def ajax_add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@demos.route('/demos/ajax_list')
def ajax_list():
    ajaxlist = []
    ajaxlist.append("a")
    ajaxlist.append("b")
    ajaxlist.append("c")
    ajaxlistlist = []
    ajaxlistlist.append(ajaxlist)
    return jsonify(ajaxlistlist)


@demos.route('/demos/datatables_ajax', methods=['GET', 'POST'])
def datatables_ajax():
    return render_template('demos/datatables_ajax.html')


@demos.route('/demos/datatables_ajax_jsondata')
def datatables_ajax_jsondata():
    ajaxlist = []
    ajaxlist.append("Tiger Nixon")
    ajaxlist.append("System Architect")
    ajaxlist.append("Edinburgh")
    ajaxlist.append("5421")
    ajaxlist.append("2011/04/25")
    ajaxlist.append("$320,800")

    ajaxlist2 = []
    ajaxlist2.append("Nixon")
    ajaxlist2.append("System Developer")
    ajaxlist2.append("Edinburgh")
    ajaxlist2.append("1234")
    ajaxlist2.append("2016/04/25")
    ajaxlist2.append("$480,800")

    ajaxlistlist = []
    ajaxlistlist.append(ajaxlist)
    ajaxlistlist.append(ajaxlist2)
    jsonmap = {"data": ajaxlistlist}
    return jsonify(jsonmap)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@demos.route('/demos/flask_wtf', methods=['GET', 'POST'])
def flask_wtf():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        admin = DemoUser(username=form.name.data)
        return redirect(url_for('.flask_wtf'))
    return render_template('demos/flask_wtf.html', form=form, name=session.get('name'))


class FlaskWtf2Form(FlaskForm):
    id = HiddenField()
    name = StringField(u'名字', validators=[DataRequired(), InputRequired()])
    ip = StringField(u'ip', validators=[DataRequired(), InputRequired(), IPAddress(ipv4=True)])
    username = StringField(u'用户名')
    businessdepart = SelectField(u'业务', coerce=int)
    submit = SubmitField(u'提交')

    def validate_name(form, field):
        if len(field.data) > 5:
            raise ValidationError('Name must be less than 5 characters')


@demos.route('/demos/flask_wtf2', methods=('GET', 'POST'))
def flask_wtf2():
    form = FlaskWtf2Form()
    form.businessdepart.choices = [(2, u'业务b'), (3, u'业务d')]
    if form.validate_on_submit():
        return render_template('demos/blank.html')
    return render_template('demos/flask_wtf2.html', form=form)


class DemoUserForm(FlaskForm):
    id = HiddenField()
    username = StringField(u'用户名', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


@demos.route('/demos/demouser', methods=['GET', 'POST'])
def demouser():
    item = DemoUser()
    form = DemoUserForm()
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        return render_template('demos/blank.html')
    return render_template('demos/normal_form.html', form=form, name=u"demouser")


BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class DemoUser2Form(ModelForm):
    class Meta:
        model = DemoUser
    submit = SubmitField(u'提交')


@demos.route('/demos/demouser_form', methods=['GET', 'POST'])
def demouser2():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        item = DemoUser.query.filter_by(id=reqid).first()
    else:
        item = DemoUser()
    form = DemoUser2Form(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        return render_template('demos/blank.html')
    return render_template('demos/normal_form.html', form=form, name=u"demouser")


@demos.route('/demos/demouser_index', methods=['GET', 'POST'])
def demouser_index():
    listnames = [u"id", u"用户名",  u"操作" ]
    return render_template('demos/datatablelist.html', listnames=listnames, formurl="/demos/demouser_form", name=u"demouser列表",
                           ajaxl="/demos/demouser_list")


@demos.route('/demos/demouser_list')
def demouser_list():
    #id,idc种类,备注
    ajaxresult = []
    for ser in DemoUser.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.username)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@demos.route('/demos/demouser_form_del', methods=['GET', 'POST'])
def demouser_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            DemoUser.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


def DemoUserQuery():
    return DemoUser.query


class DemoPostForm(FlaskForm):
    id = HiddenField()
    title = StringField(u'title', validators=[Length(max=80)])
    body = StringField(u'title')
    pub_date = StringField('pub_date')
    category_id = QuerySelectField(u'category_id', query_factory=DemoUserQuery, allow_blank=False,
                                   get_label="username")
    submit = SubmitField(u'提交')


@demos.route('/demos/demopost_index', methods=['GET', 'POST'])
def demopost_index():
    listnames = [u"id", u"title", u"body", u"pub_date", u"username",  u"操作" ]
    return render_template('demos/datatablelist.html', listnames=listnames, formurl="/demos/demopost_form", name=u"demopost列表",
                           ajaxl="/demos/demopost_list")


@demos.route('/demos/demopost_list')
def demopost_list():
    #id,title,body,pub_date,username
    ajaxresult = []
    for ser in DemoPost.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.title)
        ajaxlist.append(ser.body)
        ajaxlist.append(ser.pub_date)
        if ser.category_id is not None and ser.category_id != "":
            ajaxlist.append(DemoPost.query.filter_by(id=ser.category_id).first().username)
        else:
            ajaxlist.append("")
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@demos.route('/demos/demopost_form_del', methods=['GET', 'POST'])
def demopost_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            DemoPost.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@demos.route('/demos/demopost_form', methods=['GET', 'POST'])
def demopost_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        item = DemoPost.query.filter_by(id=reqid).first()
    else:
        item = DemoPost()
    #form = DemoPostForm(obj=item)
    form = DemoPostForm()
    if form.validate_on_submit():
        print form.data
        form.populate_obj(item)
        db.session.add(item)
        print item.__dict__
        print item.category_id.username
        db.session.commit()
        return render_template('demos/blank.html')
    return render_template('demos/normal_form.html', form=form, name=u"demopost")