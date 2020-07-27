# -*- coding:utf-8 -*-
"""
__author__ = 'nieyabin'
"""
from ..dao import dao_user
# from config import SYS_ADMIN_INIT


def get_user_by_id(user_id):
    return dao_user.get_user_by_mobile(user_id)


def get_user_by_mobile(mobile):
    return dao_user.get_user_by_mobile(mobile)


def get_user_by_email(email):
    return dao_user.get_user_by_email(email)


# def create_sys_admin(ip):
#     data = SYS_ADMIN_INIT
#     print '==============data=========='
#     print data
#     return dao_user.create_sys_admin(data, ip)

def create_sys_admin_omcp(data, ip):
    return dao_user.create_sys_admin(data, ip)

def del_user_by_id(user_id):
    return dao_user.del_user_by_id(user_id)


def create_user(data):
    return dao_user.create_user(data)