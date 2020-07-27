# -*- coding: utf-8 -*-
import uuid
import datetime
import random
import string
import hashlib
import time
import json
# import jwt
# from config import AUTH_TOKEN_SECRET, AUTH_REFRESH_TOKEN_SECRET


def convert_to_dict(obj):
    """把Object对象转换成Dict对象"""
    if obj is None:
        return {}
    dict = {}
    obj._sa_instance_state = ''
    dict.update(obj.__dict__)
    return dict


def com_obj_dict(objs):
    data = []
    if len(objs) > 0:
        count = len(objs)
        for obj in objs:
            obj = convert_to_dict(obj)
            data.append(obj)
    else:
        count = 0
    return data, count


def make_uuid(types=None):
    """
    根据字段types生成不同的UUID
    标识符	说明	样例
    O	机构UUID	O-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    R	教室UUID	R-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    C	NDS-Control UUID	C-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    V	NDS-View UUID	V-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    S	Screen UUID	S-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    Z	课程UUID	Z-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    U	单元（课）UUID	U-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    E	资源UUID	E-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    D	学员设备UUID	D-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    I	表示教室中教师的教学iPad设备的UUID	I-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    T	表示教师的其他设备UUID	T-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    L	表示直播频道UUID	L-C2A28D93-4C66-4920-80C1-BF8F5BFB5595
    :param types: 
    :return: 
    """
    if types:
        return "-".join([types, str(uuid.uuid1())]).upper()
    else:
        return str(uuid.uuid1()).upper()


def generate_password(passwd):
    """
    salt + 明文密码 加密20次后存库
    :param passwd: 明文密码
    :return: 
    """
    password_salt = generate_salt()
    password = passwd + password_salt
    for i in range(20):
        password = hashlib.sha512(password).hexdigest()
    return password_salt, password


def generate_password_from_edumin(passwd, password_salt):
    password = passwd + password_salt
    for i in range(20):
        password = hashlib.sha512(password).hexdigest()
    return password_salt, password


def generate_salt():
    """
    随机生成20位密码salt
    :return: 
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, 20))


def generate_class_room_num():
    """
    "JS-0086-xxxxxx-xxxx"
    :return:
    """
    return '-'.join(['JS-0086', ''.join(random.sample(string.digits, 6)), ''.join(random.sample(string.digits, 4))])


def random_id():
    """当前 时间戳+四位随机数 生成主键ID"""
    time_now = str(time.time()).replace('.', '')
    rand_int = random.randint(1000, 9999)
    key_id = ''.join([time_now, str(rand_int)])
    return int(key_id)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def convert_to_json(data):
    return json.dumps(data, cls=CJsonEncoder)


# def refresh_encode(data):
#     """
#     加密传输的数据
#     :param data: dict
#     :return:
#     """
#     data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=30)
#     return jwt.encode(data, AUTH_REFRESH_TOKEN_SECRET, algorithm='HS256')


# def refresh_decode(refresh_token):
#     """
#     解密传输的数据
#     :param refresh_token: 加密长字符串
#     :return:
#     """
#     try:
#         data = jwt.decode(refresh_token, AUTH_REFRESH_TOKEN_SECRET)
#     except Exception as e:
#         return False
#     refresh_data = dict()
#     refresh_data["user_uuid"] = data["user_uuid"]
#     refresh_data["user_phone"] = data["user_phone"]
#     return encode(refresh_data)

#
# def make_token_data(data):
#     """加密数据传输"""
#     data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
#     return jwt.encode(data, AUTH_TOKEN_SECRET, algorithm='HS256')
#
#
# def encode(data):
#     """
#     加密传输的数据
#     :param data: dict
#     :return:
#     """
#     refresh_data = data
#     data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
#     data["refresh_token"] = refresh_encode(refresh_data)
#     return jwt.encode(data, AUTH_TOKEN_SECRET, algorithm='HS256')
#
#
# def decode(data):
#     """
#     解密传输的数据
#     :param data: 加密长字符串
#     :return:
#     """
#     return jwt.decode(data, AUTH_TOKEN_SECRET)
