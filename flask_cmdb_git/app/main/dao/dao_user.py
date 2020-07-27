# -*- coding:utf-8 -*-
"""
__author__ = 'nieyabin'
"""
from app.main.models import User, db_save, db_commit, db_delete
from app.util import common


def get_user():
    """
    获取所有用户
    :return: 
    """
    user = User.query.all()
    return common.com_obj_dict(user)


def get_user_by_id(user_id):
    """
    根据用户id查询用户个人信息
    :param user_id: 
    :return: 返回用户信息
    """
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email):
    """
    根据用户email查询用户个人信息
    :param email: 
    :return: 
    """
    return User.query.filter_by(email=email).first()


def get_user_by_mobile(mobile):
    """
    mobile
    :param mobile: 
    :return: 
    """
    return User.query.filter_by(mobile=mobile).first()


def create_sys_admin(data, ip):
    exit_users = []
    success = False
    print data
    for us in data:
        print '=============mobile======'
        print us['mobile'], type(us['mobile'])
        tel = get_user_by_mobile(us["mobile"])
        if not tel:
            user = User(user_name=us["user_name"], nick_name=us["nick_name"], mobile=us["mobile"],
                        passwd=us["password"])
            db_save(user)
        else:
            exit_users.append(us["mobile"])
        success = True
    msg = str(len(exit_users)) + u"个用户已经存在:" + str(exit_users)
    return success, msg


def create_user(data):
    """
    注册用户
    :param data:
    :return:
    """
    exit_users = []
    success = False
    print '================data======='
    print data
    if data:
        tel = get_user_by_mobile(data["mobile"])
        if not tel:
            user = User(user_name=data["user_name"], nick_name=data["nick_name"], mobile=data["mobile"],
                        passwd=data["password"])
            db_save(user)
        else:
            exit_users.append(data["mobile"])
        success = True
        msg = str(len(exit_users)) + u"个用户已经存在:" + str(exit_users)
    else:
        msg = u'提交信息有误'

    return success, msg


def update_sys_admin(data):
    user = get_user_by_id(data["user_id"])
    user.login_time = data["login_time"]
    user.login_ip = data["login_ip"]
    db_save(user)

def del_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db_delete(user)
        success = True
        msg = u'成功删除'
    else:
        success = True
        msg = u'删除失败'

    return success, msg
