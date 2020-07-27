# coding:utf-8
from flask import render_template, jsonify

from . import devices
from .models import *
from ..util.none import check_not_none, return_value


@devices.route('/devices/servers_index', methods=['GET', 'POST'])
def server_index():
    listnames = [u"id", u"序列号", u"业务类型", u"服务器类型", u"ip", u"ip2", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/server_form", name=u"服务器列表",
                           ajaxl="/devices/servers_list")


@devices.route('/devices/servers_list')
def servers_list():
    ajaxresult = []
    for ser in Server.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        device = Device.query.filter_by(deviceTypeId=ser.id).first()
        if check_not_none(device) and check_not_none(device.serialNo):
            ajaxlist.append(device.serialNo)
        else:
            ajaxlist.append("")
        if check_not_none(ser.business_id):
            ajaxlist.append(Business.query.filter_by(id=ser.business_id).first().name)
        else:
            ajaxlist.append("")
        if check_not_none(ser.serverType_id):
            ajaxlist.append(ServerType.query.filter_by(id=ser.serverType_id).first().name)
        else:
            ajaxlist.append("")
        if check_not_none(device) and check_not_none(device.ip):
            ajaxlist.append(device.ip)
        else:
            ajaxlist.append("")
        if check_not_none(device) and check_not_none(device.ip2):
            ajaxlist.append(device.ip2)
        else:
            ajaxlist.append("")
        ajaxresult.append(ajaxlist)
    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/devices_index', methods=['GET', 'POST'])
def devices_index():
    listnames = [u"id", u"设备类型", u"序列号", u"功率", u"购买日期", u"保修时间", u"ipv4 ip", u"ipv4 ip2", u"位置", u"机柜", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/device_form", name=u"设备列表",
                           ajaxl="/devices/devices_list")


@devices.route('/devices/devices_list')
def devices_list():
    ajaxresult = []
    for ser in Device.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        if ser.deviceType != "" and ser.deviceType is not None:
            if ser.deviceType == 1:
                ajaxlist.append(u"服务器")
            elif ser.deviceType == 2:
                ajaxlist.append(u"网络设备")
            elif ser.deviceType == 3:
                ajaxlist.append(u"安全设备")
            else:
                ajaxlist.append(u"普通设备")
        else:
            ajaxlist.append("")
        ajaxlist.append(ser.serialNo)
        ajaxlist.append(ser.designedPower)
        ajaxlist.append(ser.purchaseDate)
        ajaxlist.append(ser.warrantyTime)
        ajaxlist.append(ser.ip)
        ajaxlist.append(ser.ip2)
        ajaxlist.append(ser.position)
        if ser.carbinet_id != "" and ser.carbinet_id is not None:
            ajaxlist.append(Cabinet.query.filter_by(id=ser.carbinet_id).first().name)
        else:
            ajaxlist.append("")
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/business_index', methods=['GET', 'POST'])
def business_index():
    listnames = [u"id", u"业务名称", u"注释", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/business_form", name=u"业务列表",
                           ajaxl="/devices/business_list")


@devices.route('/devices/business_list')
def business_list():
    # id,业务名称,注释
    ajaxresult = []
    for ser in Business.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.name)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/devicemanufacturer_index', methods=['GET', 'POST'])
def devicemanufacturer_index():
    listnames = [u"id", u"生产厂商", u"设备型号", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/devicemanufacturer_form",
                           name=u"服务器生产厂家列表",
                           ajaxl="/devices/devicemanufacturer_list")


@devices.route('/devices/devicemanufacturer_list')
def devicemanufacturer_list():
    # id,生产厂商,设备型号,备注
    ajaxresult = []
    for ser in DeviceManufacturer.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.manufacturer)
        ajaxlist.append(ser.devicename)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/cpumodel_index', methods=['GET', 'POST'])
def cpumodel_index():
    listnames = [u"id", u"型号", u"频率", u"核心数量", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/cpumodel_form",
                           name=u"cpu型号列表",
                           ajaxl="/devices/cpumodel_list")


@devices.route('/devices/cpumodel_list')
def cpumodel_list():
    # id,型号,频率,核心数量,备注
    ajaxresult = []
    for ser in CpuModel.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.model)
        ajaxlist.append(ser.frequency)
        ajaxlist.append(ser.corenum)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/memorymodel_index', methods=['GET', 'POST'])
def memorymodel_index():
    listnames = [u"id", u"频率", u"内存代", u"总容量", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/memorymodel_form",
                           name=u"内存型号列表",
                           ajaxl="/devices/memorymodel_list")


@devices.route('/devices/memorymodel_list')
def memorymodel_list():
    ajaxresult = []
    for ser in MemoryModel.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.frequency)
        ajaxlist.append(ser.memGen)
        ajaxlist.append(ser.size)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/cabinet_index', methods=['GET', 'POST'])
def cabinet_index():
    listnames = [u"id", u"最大功率", u"机房", u"名称", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/cabinet_form", name=u"机柜列表",
                           ajaxl="/devices/cabinet_list")


@devices.route('/devices/cabinet_list')
def cabinet_list():
    # id,名称,最大功率,机房,备注
    ajaxresult = []
    for ser in Cabinet.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.name)
        ajaxlist.append(ser.designedpower)
        if ser.idc != "":
            ajaxlist.append(Idc.query.filter_by(id=ser.idc).first().name)
        else:
            ajaxlist.append("")
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/idc_type_index', methods=['GET', 'POST'])
def idc_type_index():
    listnames = [u"id", u"idc种类", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/idc_type_form",
                           name=u"机房类型列表",
                           ajaxl="/devices/idc_type_list")


@devices.route('/devices/idc_type_list')
def idc_type_list():
    # id,idc种类,备注
    ajaxresult = []
    for ser in Idc_type.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.desc)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/idc_index', methods=['GET', 'POST'])
def idc_index():
    listnames = [u"id", u"机房名称", u"位置", u"机房类型信息", u"机房详细地址", u"机柜数量", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/idc_form", name=u"机房列表",
                           ajaxl="/devices/idc_list")


@devices.route('/devices/idc_list')
def idc_list():
    # id,机房名称,位置,机房类型信息,机房详细地址,机柜数量,备注
    ajaxresult = []
    for ser in Idc.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.name)
        ajaxlist.append(ser.position)
        if ser.idc_type_id != "":
            ajaxlist.append(Idc_type.query.filter_by(id=ser.idc_type_id).first().desc)
        else:
            ajaxlist.append("")
        ajaxlist.append(ser.address)
        ajaxlist.append(ser.serverCabinetNum)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


##todo
@devices.route('/devices/example_index', methods=['GET', 'POST'])
def example_index():
    listnames = [u"id", u"生产厂商", u"设备型号", u"备注", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/devicemanufacturer_form",
                           name=u"业务列表",
                           ajaxl="/devices/devicemanufacturer_list")


@devices.route('/devices/example_list')
def example_list():
    # id,生产厂商,设备型号,备注
    ajaxresult = []
    for ser in DeviceManufacturer.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.manufacturer)
        ajaxlist.append(ser.devicename)
        ajaxlist.append(ser.comment)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/servertype_index', methods=['GET', 'POST'])
def servertype_index():
    listnames = [u"id", u"设备类型名称", u"内存插槽数量", u"内存数量", u"cpu数量", u"cpu型号", u"生产厂家", u"型号名称", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/servertype_form",
                           name=u"服务器类型列表",
                           ajaxl="/devices/servertype_list")


@devices.route('/devices/servertype_list')
def servertype_list():
    ajaxresult = []
    for ser in ServerType.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.name)
        ajaxlist.append(ser.memorySlotNum)
        ajaxlist.append(ser.memoryNum)
        ajaxlist.append(ser.cpunum)
        if ser.cpu_id != "":
            ajaxlist.append(CpuModel.query.filter_by(id=ser.cpu_id).first().model)
        else:
            ajaxlist.append("")
        ajaxlist.append(ser.manufacturer)
        ajaxlist.append(ser.deviceTypeName)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/disk_index', methods=['GET', 'POST'])
def disk_index():
    listnames = [u"id", u"磁盘容量大小", u"转速", u"存储类型", u"生产厂家", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/disk_form", name=u"硬盘类型列表",
                           ajaxl="/devices/disk_list")


@devices.route('/devices/disk_list')
def disk_list():
    ajaxresult = []
    for ser in Disk.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(ser.size)
        ajaxlist.append(ser.rpmSpeed)
        ajaxlist.append(ser.storageType)
        ajaxlist.append(ser.manufacturer)
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/systemconfiginfo_index', methods=['GET', 'POST'])
def systemconfiginfo_index():
    listnames = [u"id", u"ip", u"saltid", u"mac", u"selinux", u"sshd", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/systemconfiginfo_form",
                           name=u"系统配置信息列表", ajaxl="/devices/systemconfiginfo_list")


@devices.route('/devices/systemconfiginfo_list')
def systemconfiginfo_list():
    ajaxresult = []
    for ser in SystemConfigInfo.query.all():
        ajaxlist = []
        ajaxlist.append(return_value(ser.id))
        ajaxlist.append(return_value(ser.ip))
        ajaxlist.append(return_value(ser.saltid))
        ajaxlist.append(return_value(ser.macAddress))
        ajaxlist.append(return_value(ser.selinuxEnabled))
        ajaxlist.append(return_value(ser.sshdVer))
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/department_index', methods=['GET', 'POST'])
def department_index():
    listnames = [u"id", u"名称", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/department_form",
                           name=u"部门信息列表", ajaxl="/devices/department_list")


@devices.route('/devices/department_list')
def department_list():
    ajaxresult = []
    for ser in Department.query.all():
        ajaxlist = []
        ajaxlist.append(return_value(ser.id))
        ajaxlist.append(return_value(ser.name))
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/patchhistory_index', methods=['GET', 'POST'])
def patchhistory_index():
    listnames = [u"id", u"补丁名称", u"补丁日期", u"程序", u"执行人", u"业务", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/patchhistory_form",
                           name=u"补丁历史列表", ajaxl="/devices/patchhistory_list")


@devices.route('/devices/patchhistory_list')
def patchhistory_list():
    ajaxresult = []
    for ser in PatchHistory.query.all():
        ajaxlist = []
        ajaxlist.append(ser.id)
        ajaxlist.append(return_value(ser.patchName))
        ajaxlist.append(return_value(ser.patchDate))
        ajaxlist.append(return_value(ser.appName))
        ajaxlist.append(return_value(ser.executor))
        if check_not_none(ser.business_id):
            ajaxlist.append(Business.query.filter_by(id=ser.business_id).first().name)
        else:
            ajaxlist.append("")
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)


@devices.route('/devices/businessinfo_index', methods=['GET', 'POST'])
def businessinfo_index():
    listnames = [u"id", u"业务名称(业务2类)", u"业务起始时间", u"业务结束时间", u"关键应用(包含版本信息)", u"业务联系人", u"操作"]
    return render_template('devices/devices.html', listnames=listnames, formurl="/devices/businessinfo_form",
                           name=u"二级业务信息列表", ajaxl="/devices/businessinfo_list")


@devices.route('/devices/businessinfo_list')
def businessinfo_list():
    ajaxresult = []
    for ser in BusinessInfo.query.all():
        ajaxlist = []
        ajaxlist.append(return_value(ser.id))
        ajaxlist.append(return_value(ser.businessName))
        ajaxlist.append(return_value(ser.businessStart))
        ajaxlist.append(return_value(ser.businessEnd))
        ajaxlist.append(return_value(ser.keyApp))
        ajaxlist.append(return_value(ser.relevantPerson))
        ajaxresult.append(ajaxlist)

    jsonmap = {"data": ajaxresult}
    return jsonify(jsonmap)
