# -*- coding: utf-8 -*-


def check_not_none(param):
    if param is None or param == "":
        return False
    else:
        return True

def return_value(param):
    if param is None or param == "":
        return ""
    else:
        return param
