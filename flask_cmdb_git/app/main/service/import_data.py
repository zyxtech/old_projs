# -*- encoding:utf-8 -*-
"""
__author__=nieyabin
"""

import xlrd
from app.main.dao.dao_import_data import save_data


def excel(fname):
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "no sheet in %s named Sheet1" % fname
# 获取行数
    nrows = sh.nrows
    print '=======nrows=========', nrows
# 获取列数
    ncols = sh.ncols

# 获取第一行第一列数据
    cell_value = sh.cell_value(0, 1)
    print cell_value

    row_list = []
# 获取各行数据

    for i in range(1, nrows):
        row_data = sh.row_values(i)

        save_data(row_data[0], row_data[1])
        row_list.append(row_data)


    return row_list
