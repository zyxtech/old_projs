# -*- encoding:utf-8 -*-
"""
__author__=nieyabin
"""


from ..models import User, db_save
from app.util import common


def save_data(user_name, nick_name):
    user = User(user_name=user_name, nick_name=nick_name)
    try:
        db_save(user)
        return True, u"保存成功"
    except Exception as e:
        return False, u"保存失败"