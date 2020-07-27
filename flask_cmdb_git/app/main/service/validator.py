# -*- coding: utf-8 -*-
"""
__author__ = 'nieyabin'
"""
import time
import datetime
import re
import hashlib
# from ..dao import dao_classroom
from app.util import common


class DataValidator:
    validate_type = None

    def __init__(self):
        self.validate_type = "json"

    def validate(self, data):
            return self.handler(data)

    @staticmethod
    def handler(data):
        if not isinstance(data, dict):
            return False
        return True

    @staticmethod
    def set_default_value(data, key, value):
        """为可选字段设置默认值(如字段不存在)"""
        if key in data.iterkeys():
            data[key] = value

    @staticmethod
    def set_value(data, key, value):
        """设置字段值"""
        data[key] = value

    @staticmethod
    def must_has_value(data, keys):
        """字段不能为空"""
        rv = True
        for key in keys:
            if data[key] in ["", None]:
                rv = False
                break
        return rv

    @staticmethod
    def must_has_key(data, keys):
        """检测数据中是否包含必须字段"""
        rv = True
        for k in keys:
            if k not in data.iterkeys():
                rv = False
                break
        return rv


class OmcpDataValidator(DataValidator):
    def validate_login_log(self, data):
        """传入的笔记数据验证"""
        if self.must_has_key(data, ["user_id", "ip"]):
            return data
        else:
            return False

    def validate_post_passwd(self, data):
        """验证密码"""
        if self.must_has_key(data, ["password"]):
            return data
        else:
            return False

    def validate_post_org(self, data):
        """验证添加机构信息"""
        if self.must_has_key(data, ["org_name", "org_uuid", "contacts", "contact_phone", "web_domain"]):
            if "create_time" not in data.iterkeys():
                self.set_default_value(data, "create_time", format_stamp_local_time())
            return data
        else:
            return False

    def validate_post_sys_admin(self, data):
        """验证添加管理员信息"""
        if self.must_has_key(data, ["user_uuid", "user_phone", "org_uuid", "user_password"]):
            self.set_default_value(data, "created_time", format_stamp_local_time())
            if not self.must_has_value(data, ["user_phone", "org_uuid", "user_password"]):
                return False
            password_salt, password = common.generate_password(data["user_password"])
            self.set_value(data, "password", data["user_password"])
            self.set_value(data, "password_salt", password_salt)
            self.set_value(data, "user_password", password)
            self.set_value(data, "role", 5)
            return data
        else:
            return False

    def validate_update_sys_admin(self, data):
        """验证修改管理员密码"""
        if self.must_has_key(data, ["user_uuid", "user_password"]):
            if not self.must_has_value(data, ["user_password"]):
                return False
            password_salt, password = common.generate_password(data["user_password"])
            self.set_value(data, "password_salt", password_salt)
            self.set_value(data, "user_password", password)
            return data
        else:
            return False

    def validate_post_sync_sys_admin(self, data):
        """验证添加管理员信息"""
        if self.must_has_key(data, ["user_uuid", "user_phone", "org_uuid", "user_password", "password_salt"]):
            if not self.must_has_value(data, ["user_phone", "org_uuid", "user_password"]):
                return False
            return data
        else:
            return False

    def validate_post_app_version(self, data):
        """验证应用版本信息"""
        print "====validate_post_app_version data===="
        print data
        if self.must_has_key(data, ["app_uuid", "app_name", "app_ver", "app_md5", "file_url", "is_newest"]):
            self.set_default_value(data, "update_time", format_stamp_local_time())
            print "====after validate_post_app_version data===="
            print data
            return data
        else:
            return False

    def validate_update_org(self, data):
        """验证更新机构"""
        if self.must_has_key(data, ["org_uuid"]):
            return data
        else:
            return False

    def validate_post_log(self, data):
        """验证添加日志信息"""
        if self.must_has_key(data, ["user_id", "user_name", "operate", "content"]):
            return data
        else:
            return False

    def validate_post_app_setting(self, data):
        """验证应用配置信息"""
        if self.must_has_key(data,  ["org_uuid", "name", "value"]):
            if not self.must_has_value(data, ["org_uuid", "name", "value"]):
                return False
            return data
        else:
            return False

    def validate_admin_sync_from_mpoc(self, data):
        """验证添加管理员信息"""
        if self.must_has_key(data, ["user_uuid", "user_phone", "org_uuid", "password", "password_salt", "role"]):
            self.set_default_value(data, "created_time", format_stamp_local_time())
            if not self.must_has_value(data, ["user_phone", "org_uuid", "password"]):
                return False
            password_salt, user_password = common.generate_password_from_edumin(data["password"], data["password_salt"])
            self.set_value(data, "user_password", user_password)
            return data
        else:
            return False


    def validate_post_screen(self, data):
        """验证屏幕信息"""
        if self.must_has_key(data,  ["org_uuid", "room_uuid", "sc_uuid", "screen_uuid"]):
            if not self.must_has_value(data, ["org_uuid", "room_uuid", "sc_uuid", "screen_uuid"]):
                return False
            return data
        else:
            return False

    def validate_post_screen2(self, data):
        """验证屏幕信息"""
        if self.must_has_key(data,  ["org_uuid", "room_uuid", "sc_uuid"]):
            if not self.must_has_value(data, ["org_uuid", "room_uuid", "sc_uuid"]):
                return False
            return data
        else:
            return False

def format_stamp_local_time():
    """
    时间戳格式化
    :param val:
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def validate_login_user(username):
    email = re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]')
    tel = re.compile('^0\d{2,3}\d{7,8}$|^1[23589]\d{9}$|^147\d{8}')
    id_card = re.compile('^(\d{15}$)|(^\d{17}([0-9]|X|x)$)')
    wechat_openid = re.compile('^[\w\-]{28}$')
    wechat_unionid = re.compile('^[\w\-]{29}$')

    if email.match(username) and len(username) > 7:
        return "email"

    if tel.match(username):
        return "mobile"

    if id_card.match(username):
        return "id_card"

    if wechat_openid.match(username):
        return "wechat_openid"

    if wechat_unionid.match(username):
        return "wechat_unionid"

    return False


def validate_login_password(user, password):
    success = False
    if user is None:
        msg = u"该用户不存在该系统中!"
        return success, msg
    if user is not None and user.verify_password(password):
        success = True
        msg = u"登录成功"
        return success, msg
    else:
        msg = u"您输入的密码有误!"
    return success, msg





def validation_passwd(password_salt, crypted_password, passwd):
    """
    密码验证
    :param password_salt: 数据库存储的
    :param crypted_password: 数据库存储的密码
    :param passwd: 输入的密码
    :return:
    """
    status = False
    a_salt = passwd + password_salt
    for i in range(20):
        a_salt = hashlib.sha512(a_salt).hexdigest()
    if a_salt == crypted_password:
        status = True
    return status


def validate_screen_submit(data):
    data["screen_uuid"] = common.make_uuid()
    if data['sc_uuid'] == '':
        msg = u'屏幕控制服务不能为空'
    else:
        msg = u'success'

    return msg

def validate_update_org_info(data):
    success = True
    msg = u'success'
    telp = re.compile('^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^147\d{8}')
    domail = re.compile('(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
    domail2 = re.compile('^http://(?i)([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]|[\/]{2,}$')
    d2 = domail2.match(data["web_domain"])
    d1 = domail.match(data["web_domain"])
    t = telp.match(data["contact_phone"])

    if data['org_name'] in [None, u'', '']:
        msg = u'机构名称不能为空'
        success = False
    elif data['contacts'] in [None, u'', '']:
        msg = u'联系人不能为空'
        success = False
    elif not d1:
        if not d2:
            msg = u'域名格式有误'
            success = False
        else:
            success = True
            msg = u'success'

    if not t:
        msg = u'联系电话格式有误'
        success = False

    return success, msg
