# coding:utf-8
from flask import render_template, redirect, request, jsonify

from . import devices
from .forms import *
from .models import DeviceManufacturer, Server, Business, MemoryModel, CpuModel, Cabinet, Idc_type, Idc, Device, \
    ServerType, Disk, SystemConfigInfo, Department, PatchHistory, BusinessInfo
from .. import db


@devices.route('/devices/server_form_del', methods=['GET', 'POST'])
def server_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Server.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/server_form', methods=['GET', 'POST'])
def server_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = ServerDeviceForm()

    form.business_id.choices = [(g.id, g.name) for g in Business.query.order_by("name")]
    form.carbinet_id.choices = [(g.id, g.name) for g in Cabinet.query.order_by("name")]
    form.serverType_id.choices = [(g.id, g.name) for g in ServerType.query.order_by("name")]
    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            device = Device.query.filter_by(id=int(form.id.data)).first()
        else:
            device = Device()
        form.populate_obj(device)
        device.deviceType = 1

        if not (form.id.data is None or form.id.data == ""):
            ser = Server.query.filter_by(id=int(form.deviceTypeId.data)).first()
            ser.business_id = form.business_id.data
            ser.serverType_id = form.serverType_id.data
            db.session.commit()
        else:
            ser = Server()
            ser.business_id = form.business_id.data
            ser.serverType_id = form.serverType_id.data
            if device.id == u'':
                device.id = None
            db.session.add(ser)
            db.session.commit()
            device.deviceTypeId = ser.id
            db.session.add(device)
            db.session.commit()
        return redirect('devices/servers_index')
    else:
        if not reqid == 0:
            server = Server.query.filter_by(id=reqid).first()
            device = Device.query.filter_by(deviceTypeId=server.id).first()
            form = ServerDeviceForm(obj=device)
            form.business_id.data = server.business_id
            form.serverType_id.data = server.serverType_id
            form.business_id.choices = [(g.id, g.name) for g in Business.query.order_by("name")]
            form.carbinet_id.choices = [(g.id, g.name) for g in Cabinet.query.order_by("name")]
            form.serverType_id.choices = [(g.id, g.name) for g in ServerType.query.order_by("name")]
    return render_template('devices/normal_form.html', form=form, name=u"服务器")


@devices.route('/devices/device_form_del', methods=['GET', 'POST'])
def device_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            device = Device.query.filter_by(id=reqid).first()
            if Server.query.filter_by(id=device.deviceTypeId).first() is not None:
                jsonmap = {"data": "failed", "info": u"请删除相关服务器后再删除设备"}
            else:
                Device.query.filter_by(id=reqid).delete()
                db.session.commit()
                jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/device_form', methods=['GET', 'POST'])
def device_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = DeviceForm()
    form.carbinet_id.choices = [(g.id, g.name) for g in Cabinet.query.order_by("name")]

    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            device = Device.query.filter_by(id=int(form.id.data)).first()
        else:
            device = Device()
        form.populate_obj(device)
        if not (form.id.data is None or form.id.data == ""):
            db.session.commit()
        else:
            if device.id == u'':
                device.id = None
            device.deviceType = 0
            db.session.add(device)
            db.session.commit()
        return redirect('devices/devices_index')
    else:
        if not reqid == 0:
            device = Device.query.filter_by(id=reqid).first()
            form = DeviceForm(obj=device)
            form.carbinet_id.choices = [(g.id, g.name) for g in Cabinet.query.order_by("name")]
    return render_template('devices/normal_form.html', form=form, name=u"设备")


@devices.route('/devices/business_form', methods=['GET', 'POST'])
def business_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = BusinessForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            business = Business.query.filter_by(id=int(form.id.data)).first()
        else:
            business = Business()
        business.name = form.name.data
        business.comment = form.comment.data
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(business)
            db.session.commit()
        return redirect('/devices/business_index')
    else:
        if (not reqid == 0):
            business = Business.query.filter_by(id=reqid).first()
            form.id.data = business.id
            form.name.data = business.name
            form.comment.data = business.comment
    return render_template('devices/normal_form.html', form=form, name=u"业务")


@devices.route('/devices/business_form_del', methods=['GET', 'POST'])
def business_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Business.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/devicemanufacturer_form', methods=['GET', 'POST'])
def devicemanufacturer_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = DeviceManufacturerForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            devicemanufacturer = DeviceManufacturer.query.filter_by(id=int(form.id.data)).first()
            devicemanufacturer.manufacturer = form.manufacturer.data
            devicemanufacturer.devicename = form.devicename.data
            devicemanufacturer.comment = form.comment.data
            db.session.commit()
        else:
            devicemanufacturer = DeviceManufacturer()
            devicemanufacturer.manufacturer = form.manufacturer.data;
            devicemanufacturer.devicename = form.devicename.data;
            devicemanufacturer.comment = form.comment.data
            db.session.add(devicemanufacturer)
            db.session.commit()
        return redirect('devices/devicemanufacturer_index')
    else:
        if (not reqid == 0):
            devicemanufacturer = DeviceManufacturer.query.filter_by(id=reqid).first()
            form.id.data = devicemanufacturer.id
            form.manufacturer.data = devicemanufacturer.manufacturer
            form.devicename.data = devicemanufacturer.devicename
            form.comment.data = devicemanufacturer.comment

    return render_template('devices/normal_form.html', form=form, name=u"服务器生产厂家")


@devices.route('/devices/devicemanufacturer_form_del', methods=['GET', 'POST'])
def devicemanufacturer_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            DeviceManufacturer.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/cpumodel_form', methods=['GET', 'POST'])
def cpumodel_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = CpuModelForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            cpumodel = CpuModel.query.filter_by(id=int(form.id.data)).first()
        else:
            cpumodel = CpuModel()
        cpumodel.model = form.model.data
        cpumodel.frequency = form.frequency.data
        cpumodel.corenum = form.corenum.data
        cpumodel.comment = form.comment.data
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(cpumodel)
            db.session.commit()
        return redirect('devices/cpumodel_index')
    else:
        if (not reqid == 0):
            cpumodel = CpuModel.query.filter_by(id=reqid).first()
            form.model.data = cpumodel.model
            form.frequency.data = cpumodel.frequency
            form.corenum.data = cpumodel.corenum
            form.comment.data = cpumodel.comment
    return render_template('devices/normal_form.html', form=form, name=u"cpu")


@devices.route('/devices/cpumodel_form_del', methods=['GET', 'POST'])
def cpumodel_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            CpuModel.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/memorymodel_form', methods=['GET', 'POST'])
def memorymodel_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = MemoryModelForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            memorymodel = MemoryModel.query.filter_by(id=int(form.id.data)).first()
        else:
            memorymodel = MemoryModel()
        form.populate_obj(memorymodel)
        if memorymodel.id == u"":
            memorymodel.id = None
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(memorymodel)
            db.session.commit()
        return redirect('devices/memorymodel_index')
    else:
        if (not reqid == 0):
            memorymodel = MemoryModel.query.filter_by(id=reqid).first()
            form = MemoryModelForm(obj=memorymodel)
    return render_template('devices/normal_form.html', form=form, name=u"内存")


@devices.route('/devices/memorymodel_form_del', methods=['GET', 'POST'])
def memorymodel_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            MemoryModel.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/cabinet_form', methods=['GET', 'POST'])
def cabinet_form():
    reqid = 0

    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = CabinetForm()
    form.idc_id.choices = [(g.id, g.name) for g in Idc.query.order_by("name")]
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            cabinet = Cabinet.query.filter_by(id=int(form.id.data)).first()
        else:
            cabinet = Cabinet()
        print form.data.items()
        cabinet.designedpower = form.designedpower.data
        cabinet.idc = int(form.idc_id.data)
        cabinet.name = form.name.data
        cabinet.comment = form.comment.data
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(cabinet)
            db.session.commit()
        return redirect('devices/cabinet_index')
    else:
        if (not reqid == 0):
            cabinet = Cabinet.query.filter_by(id=reqid).first()
            form.id.data = cabinet.id
            form.designedpower.data = cabinet.designedpower
            form.idc_id.data = cabinet.idc
            form.name.data = cabinet.name
            form.comment.data = cabinet.comment

    return render_template('devices/normal_form.html', form=form, name=u"机柜")


@devices.route('/devices/cabinet_form_del', methods=['GET', 'POST'])
def cabinet_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Cabinet.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/idc_type_form', methods=['GET', 'POST'])
def idc_type_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = Idc_typeForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            idc_type = Idc_type.query.filter_by(id=int(form.id.data)).first()
        else:
            idc_type = Idc_type()
        idc_type.desc = form.desc.data
        idc_type.comment = form.comment.data
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(idc_type)
            db.session.commit()
        return redirect('devices/idc_type_index')
    else:
        if (not reqid == 0):
            idc_type = Idc_type.query.filter_by(id=reqid).first()
            form = Idc_typeForm(obj=idc_type)
    return render_template('devices/normal_form.html', form=form, name=u"机房类型")


@devices.route('/devices/idc_type_form_del', methods=['GET', 'POST'])
def idc_type_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Idc_type.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/idc_form', methods=['GET', 'POST'])
def idc_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = IdcForm()
    form.idc_type_id.choices = [(g.id, g.desc) for g in Idc_type.query.order_by("desc")]
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            idc = Idc.query.filter_by(id=int(form.id.data)).first()
        else:
            idc = Idc()
        form.populate_obj(idc)
        if idc.id == u"":
            idc.id = None
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(idc)
            db.session.commit()
        return redirect('devices/idc_index')
    else:
        if (not reqid == 0):
            idc = Idc.query.filter_by(id=reqid).first()
            form = IdcForm(obj=idc)
            form.idc_type_id.choices = [(g.id, g.desc) for g in Idc_type.query.order_by("desc")]
    return render_template('devices/normal_form.html', form=form, name=u"机房")


@devices.route('/devices/idc_form_del', methods=['GET', 'POST'])
def idc_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Idc.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/servertype_form', methods=['GET', 'POST'])
def servertype_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = ServerTypeForm()
    form.cpu_id.choices = [(g.id, g.model) for g in CpuModel.query.order_by("model")]
    form.memorymodel_id.choices = [(g.id, g.memGen + " " + g.frequency + " " + g.size) for g in
                                   MemoryModel.query.order_by("memGen")]
    form.diskTypeAId.choices = [(g.id, g.size + " " + g.rpmSpeed + " " + g.storageType + " " + g.manufacturer) for g in
                                Disk.query.order_by("id")]
    form.diskTypeBId.choices = [(g.id, g.size + " " + g.rpmSpeed + " " + g.storageType + " " + g.manufacturer) for g in
                                Disk.query.order_by("id")]
    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            st = ServerType.query.filter_by(id=int(form.id.data)).first()
        else:
            st = ServerType()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if not (form.id.data is None or form.id.data == ""):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/servertype_index')
    else:
        if not reqid == 0:
            idc = ServerType.query.filter_by(id=reqid).first()
            form = ServerTypeForm(obj=idc)
            form.cpu_id.choices = [(g.id, g.model) for g in CpuModel.query.order_by("model")]
            form.memorymodel_id.choices = [(g.id, g.memGen + " " + g.frequency + " " + g.size) for g in
                                           MemoryModel.query.order_by("memGen")]
            form.diskTypeAId.choices = [(g.id, g.size + " " + g.rpmSpeed + " " + g.storageType + " " + g.manufacturer)
                                        for g in
                                        Disk.query.order_by("id")]
            form.diskTypeBId.choices = [(g.id, g.size + " " + g.rpmSpeed + " " + g.storageType + " " + g.manufacturer)
                                        for g in
                                        Disk.query.order_by("id")]
    return render_template('devices/normal_form.html', form=form, name=u"服务器类型")


@devices.route('/devices/servertype_form_del', methods=['GET', 'POST'])
def servertype_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            ServerType.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/disk_form', methods=['GET', 'POST'])
def disk_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = DiskForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            st = Disk.query.filter_by(id=int(form.id.data)).first()
        else:
            st = Disk()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/disk_index')
    else:
        if (not reqid == 0):
            idc = Disk.query.filter_by(id=reqid).first()
            form = DiskForm(obj=idc)
    return render_template('devices/normal_form.html', form=form, name=u"磁盘类型")


@devices.route('/devices/disk_form_del', methods=['GET', 'POST'])
def disk_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Disk.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/systemconfiginfo_form', methods=['GET', 'POST'])
def systemconfiginfo_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = SystemConfigInfoForm()
    if form.validate_on_submit():
        if (not (form.id.data is None or form.id.data == "")):
            st = SystemConfigInfo.query.filter_by(id=int(form.id.data)).first()
        else:
            st = SystemConfigInfo()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if (not (form.id.data is None or form.id.data == "")):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/systemconfiginfo_index')
    else:
        if (not reqid == 0):
            idc = SystemConfigInfo.query.filter_by(id=reqid).first()
            form = SystemConfigInfoForm(obj=idc)
    return render_template('devices/normal_form.html', form=form, name=u"系统配置信息")


@devices.route('/devices/systemconfiginfo_form_del', methods=['GET', 'POST'])
def systemconfiginfo_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            SystemConfigInfo.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/department_form', methods=['GET', 'POST'])
def department_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = DepartmentForm()
    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            st = Department.query.filter_by(id=int(form.id.data)).first()
        else:
            st = Department()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if not (form.id.data is None or form.id.data == ""):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/department_index')
    else:
        if not reqid == 0:
            idc = Department.query.filter_by(id=reqid).first()
            form = DepartmentForm(obj=idc)
    return render_template('devices/normal_form.html', form=form, name=u"部门信息")


@devices.route('/devices/department_form_del', methods=['GET', 'POST'])
def department_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            Department.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/patchhistory_form', methods=['GET', 'POST'])
def patchhistory_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = PatchHistoryForm()
    form.business_id.choices = [(g.id, g.name)
                                for g in
                                Business.query.order_by("name")]
    form.departId.choices = [(g.id, g.name)
                             for g in
                             Department.query.order_by("name")]
    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            st = PatchHistory.query.filter_by(id=int(form.id.data)).first()
        else:
            st = PatchHistory()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if not (form.id.data is None or form.id.data == ""):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/patchhistory_index')
    else:
        if not reqid == 0:
            idc = PatchHistory.query.filter_by(id=reqid).first()
            form = PatchHistoryForm(obj=idc)
            form.business_id.choices = [(g.id, g.name)
                                        for g in
                                        Business.query.order_by("name")]
            form.departId.choices = [(g.id, g.name)
                                     for g in
                                     Department.query.order_by("name")]
    return render_template('devices/normal_form.html', form=form, name=u"系统补丁信息")


@devices.route('/devices/patchhistory_form_del', methods=['GET', 'POST'])
def patchhistory_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            PatchHistory.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/businessinfo_form', methods=['GET', 'POST'])
def businessinfo_form():
    reqid = 0
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
    form = BusinessInfoForm()
    form.serverId.choices = [(g.id, g.ip)
                             for g in
                             Device.query.filter_by(deviceType=1).order_by("ip")]
    if form.validate_on_submit():
        if not (form.id.data is None or form.id.data == ""):
            st = BusinessInfo.query.filter_by(id=int(form.id.data)).first()
        else:
            st = BusinessInfo()
        form.populate_obj(st)
        if st.id == u"":
            st.id = None
        if not (form.id.data is None or form.id.data == ""):
            db.session.commit()
        else:
            db.session.add(st)
            db.session.commit()
        return redirect('devices/businessinfo_index')
    else:
        if not reqid == 0:
            idc = BusinessInfo.query.filter_by(id=reqid).first()
            form = BusinessInfoForm(obj=idc)
            form.serverId.choices = [(g.id, g.ip)
                                     for g in
                                     Device.query.filter_by(deviceType=1).order_by("ip")]
    return render_template('devices/normal_form.html', form=form, name=u"二级业务信息")


@devices.route('/devices/businessinfo_form_del', methods=['GET', 'POST'])
def businessinfo_form_del():
    jsonmap = {}
    if request.args.has_key('id'):
        reqid = request.args.get('id', 0, type=int)
        if reqid > 0:
            BusinessInfo.query.filter_by(id=reqid).delete()
            db.session.commit()
            jsonmap = {"data": "success"}
        else:
            jsonmap = {"data": "failed"}
    return jsonify(jsonmap)


@devices.route('/devices/gen_test_data', methods=['GET', 'POST'])
def gen_test_data():
    idct = Idc_type()
    idct.desc = u'联通测试机房2'
    db.session.add(idct)
    idct = Idc_type()
    idct.desc = u'移动测试机房2'
    db.session.add(idct)
    db.session.commit()

    idc = Idc()
    idc.name = u'机房1号'
    idc.position = u'天津沈阳区'
    idc.idc_type_id = idct.id
    idc.address = u'天津沈阳区2号院'
    idc.serverCabinetNum = 36
    db.session.add(idc)
    idc = Idc()
    idc.name = u'机房2号'
    idc.position = u'武汉山西区'
    idc.idc_type_id = idct.id
    idc.address = u'武汉山西区4号院'
    idc.serverCabinetNum = 24
    db.session.add(idc)
    db.session.commit()

    carb = Cabinet()
    carb.name = u'18A'
    carb.idc = idc.id
    carb.designedpower = u'750w'
    db.session.add(carb)
    carb = Cabinet()
    carb.name = u'18C'
    carb.idc = idc.id
    carb.designedpower = u'450w'
    db.session.add(carb)
    db.session.commit()

    disk = Disk()
    disk.manufacturer = u'希捷'
    disk.size = u'2t'
    disk.rpmSpeed = u'7200'
    disk.storageType = u'sata'
    db.session.add(disk)
    disk = Disk()
    disk.manufacturer = u'西数'
    disk.size = u'4T'
    disk.rpmSpeed = u'7200'
    disk.storageType = u'sata'
    db.session.add(disk)
    db.session.commit()

    cpu = CpuModel()
    cpu.model = u'E5 2670 v3'
    cpu.frequency = u'3.6G'
    cpu.corenum = 24
    db.session.add(cpu)
    cpu = CpuModel()
    cpu.model = u'E7 4270 v5'
    cpu.frequency = u'4.2G'
    cpu.corenum = 18
    db.session.add(cpu)
    db.session.commit()

    mem = MemoryModel()
    mem.frequency = u'1600'
    mem.memGen = u'3'
    mem.size = u'8G'
    db.session.add(mem)
    mem = MemoryModel()
    mem.frequency = u'2133'
    mem.memGen = u'4'
    mem.size = u'4G'
    db.session.add(mem)
    db.session.commit()

    servert = ServerType()
    servert.manufacturer = u'戴尔'
    servert.name = u'戴尔机器 大数据用'
    servert.memorymodel_id = mem.id
    servert.cpu_id = cpu.id
    servert.cpunum = 2
    servert.deviceTypeName = u'r720'
    servert.diskNum = 4
    servert.diskTypeAId = disk.id
    servert.diskTypeANum = 3
    servert.diskTypeBId = disk.id
    servert.diskTypeBNum = 4
    servert.memoryNum = 4
    servert.memorySlotNum = 8
    servert.networkadaperANum = 2
    servert.networkadaperAType = u'千兆1000M'
    servert.networkadaperBNum = 1
    servert.networkadaperBType = u'光模块10G'
    db.session.add(servert)
    servert = ServerType()
    servert.manufacturer = u'戴尔'
    servert.name = u'戴尔机器 大数据用'
    servert.memorymodel_id = mem.id
    servert.cpu_id = cpu.id
    servert.cpunum = 2
    servert.deviceTypeName = u'r720'
    servert.diskNum = 4
    servert.diskTypeAId = disk.id
    servert.diskTypeANum = 3
    servert.diskTypeBId = disk.id
    servert.diskTypeBNum = 4
    servert.memoryNum = 4
    servert.memorySlotNum = 8
    servert.networkadaperANum = 2
    servert.networkadaperAType = u'千兆1000M'
    servert.networkadaperBNum = 1
    servert.networkadaperBType = u'光模块10G'
    db.session.add(servert)
    db.session.commit()

    busi = Business()
    busi.name = u'云计算'
    busi.comment = u'测试'
    db.session.add(busi)
    busi = Business()
    busi.name = u'大数据'
    busi.comment = u'测试2'
    db.session.add(busi)
    db.session.commit()

    syscon = SystemConfigInfo()
    syscon.javaVer = u'1.8'
    syscon.ip = u'192.18.21.21'
    syscon.saltid = u'compu1'
    syscon.macAddress = u'a4:de:e0:6a:78:ef'
    syscon.systemUserList = u'root,oracle,testu'
    syscon.networkConfig = u"""1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1 \
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00\
    inet 127.0.0.1/8 scope host lo \
       valid_lft forever preferred_lft forever\
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000\
        link/ether 00:16:3e:02:04:35 brd ff:ff:ff:ff:ff:ff\
        inet 10.129.1.3/16 brd 10.129.255.255 scope global eth0\
           valid_lft forever preferred_lft forever\
    3: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN'
    syscon.networkConfig += u'link/ether 22:26:7e:62:9f:73 brd ff:ff:ff:ff:ff:ff ' 
    inet 172.30.75.0/32 scope global flannel.1
    valid_lft forever preferred_lft forever
    4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:08:6a:ed:d7 brd ff:ff:ff:ff:ff:ff
    inet 172.30.75.1/24 scope global docker0
    valid_lft forever preferred_lft forever"""
    syscon.storageMount = u"""Filesystem      Size  Used Avail Use% Mounted on\
    /dev/vda1        40G  5.6G   32G  16% /\
    devtmpfs        1.9G     0  1.9G   0% /dev\
    tmpfs           1.9G     0  1.9G   0% /dev/shm\
    tmpfs           1.9G   25M  1.9G   2% /run\
    tmpfs           1.9G     0  1.9G   0% /sys/fs/cgroup\
    tmpfs           380M     0  380M   0% /run/user/0\
    """
    syscon.rcLocal = u'touch /var/lock/subsys/local'
    syscon.firewall = u"""Chain INPUT (policy ACCEPT)
    target     prot opt source               destination 
    Chain FORWARD (policy ACCEPT)
    target     prot opt source               destination 
    DOCKER-ISOLATION  all  --  anywhere             anywhere
    DOCKER     all  --  anywhere             anywhere
    ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
    ACCEPT     all  --  anywhere             anywhere
    ACCEPT     all  --  anywhere             anywhere

    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination

    Chain DOCKER (1 references)
    target     prot opt source               destination

    Chain DOCKER-ISOLATION (1 references)
    target     prot opt source               destination
    RETURN     all  --  anywhere             anywhere"""
    syscon.journalConfig = u'normal'
    syscon.selinuxEnabled = u'yes'
    syscon.crontabList = u''
    syscon.sshdVer = u'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017'
    syscon.portsOpened = u'22'
    db.session.add(syscon)
    syscon = SystemConfigInfo()
    syscon.javaVer = u'1.8'
    syscon.ip = u'192.18.21.21'
    syscon.saltid = u'compu1'
    syscon.macAddress = u'a4:de:e0:6a:78:ef'
    syscon.systemUserList = u'root,oracle,testu'
    syscon.networkConfig = u"""1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo 
           valid_lft forever preferred_lft forever
        2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
            link/ether 00:16:3e:02:04:35 brd ff:ff:ff:ff:ff:ff
            inet 10.129.1.3/16 brd 10.129.255.255 scope global eth0
               valid_lft forever preferred_lft forever
        3: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN
    link/ether 22:26:7e:62:9f:73 brd ff:ff:ff:ff:ff:ff 
        inet 172.30.75.0/32 scope global flannel.1
        valid_lft forever preferred_lft forever
        4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:08:6a:ed:d7 brd ff:ff:ff:ff:ff:ff
        inet 172.30.75.1/24 scope global docker0
        valid_lft forever preferred_lft forever"""
    syscon.storageMount = u"""Filesystem      Size  Used Avail Use% Mounted on
        /dev/vda1        80G  5.6G   32G  16% /
        devtmpfs        11.9G     0  1.9G   0% /dev
        tmpfs           11.9G     0  1.9G   0% /dev/shm
        tmpfs           21.9G   25M  1.9G   2% /run
        tmpfs           31.9G     0  1.9G   0% /sys/fs/cgroup
        tmpfs           380M     0  380M   0% /run/user/0
        """
    syscon.rcLocal = u'touch /var/lock/subsys/local'
    syscon.firewall = u"""Chain INPUT (policy ACCEPT)
        target     prot opt source               destination 
    Chain FORWARD (policy ACCEPT)
        target     prot opt source               destination 
    DOCKER-ISOLATION  all  --  anywhere             anywhere
    DOCKER     all  --  anywhere             anywhere
    ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
    ACCEPT     all  --  anywhere             anywhere
    ACCEPT     all  --  anywhere             anywhere

    Chain OUTPUT (policy ACCEPT)
        target     prot opt source               destination

    Chain DOCKER (1 references)
        target     prot opt source               destination

    Chain DOCKER-ISOLATION (1 references)
        target     prot opt source               destination
    RETURN     all  --  anywhere             anywhere"""
    syscon.journalConfig = u'normal'
    syscon.selinuxEnabled = u'yes'
    syscon.crontabList = u''
    syscon.sshdVer = u'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017'
    syscon.portsOpened = u'22,99,103,3306'
    db.session.add(syscon)
    db.session.commit()

    ser = Server()
    ser.business_id = busi.id
    ser.serverType_id = servert.id
    db.session.add(ser)
    ser2 = Server()
    ser2.business_id = busi.id
    ser2.serverType_id = servert.id
    ser2.comment = u'comm'
    db.session.add(ser2)
    db.session.commit()

    device = Device()
    device.deviceType = 1
    device.deviceTypeId = ser.id
    device.serialNo = u'No.22212333'
    device.designedPower = u'770w'
    device.purchaseDate = u'2017-11-22'
    device.warrantyTime = u'2020-11-22'
    device.ip = u'172.8.2.33'
    device.ip2 = u'192.8.22.11'
    device.position = u'posi1'
    device.carbinet_id = carb.id
    db.session.add(device)
    device2 = Device()
    device2.deviceType = 1
    device2.deviceTypeId = ser2.id
    device2.serialNo = u'No.211212333'
    device2.designedPower = u'1080w'
    device2.purchaseDate = u'2012-11-22'
    device2.warrantyTime = u'2030-11-22'
    device2.ip = u'172.81.2.33'
    device2.ip2 = u'192.8.22.11'
    device2.position = u'posi1'
    device2.carbinet_id = carb.id
    db.session.add(device2)
    db.session.commit()

    depar = Department()
    depar.name = u"运维部门"
    db.session.add(depar)
    depar2 = Department()
    depar2.name = u'云平台开发部门'
    db.session.add(depar2)
    db.session.commit()

    phis = PatchHistory()
    phis.patchName = u'apache补丁NO222'
    phis.patchDate = u'2019-2-12'
    phis.appName = u'apache tomcat'
    phis.executor = u'张老三'
    phis.departId = depar.id
    phis.business_id = busi.id
    db.session.add(phis)
    phis = PatchHistory()
    phis.patchName = u'apache补丁NO112'
    phis.patchDate = u'2011-2-12'
    phis.appName = u'apache apache'
    phis.executor = u'张老6'
    phis.departId = depar.id
    phis.business_id = busi.id
    db.session.add(phis)
    db.session.commit()

    busiinfo = BusinessInfo()
    busiinfo.deployDir = u'/usr/local/nginx'
    busiinfo.serverId = device.id
    busiinfo.businessStart = u'2017-6-18'
    busiinfo.businessEnd = u'2019-6-18'
    busiinfo.businessName = u'nginx 批量部署业务'
    busiinfo.confDir = u'/etc/nginx/nginx.conf'
    busiinfo.ports = u'80,443'
    busiinfo.keyApp = u'nginx'
    busiinfo.relevantPerson = u'王四'
    db.session.add(busiinfo)
    busiinfo = BusinessInfo()
    busiinfo.deployDir = u'/usr/local/tomcat'
    busiinfo.serverId = device.id
    busiinfo.businessStart = u'2017-6-18'
    busiinfo.businessEnd = u'2018-1-18'
    busiinfo.businessName = u'tomcat 批量部署业务'
    busiinfo.confDir = u'/etc/tomcat/tomcat.conf'
    busiinfo.ports = u'80,443'
    busiinfo.keyApp = u'tomcat'
    busiinfo.relevantPerson = u'王四'
    db.session.add(busiinfo)
    db.session.commit()

    db.session.commit()

    return render_template('index.html')
