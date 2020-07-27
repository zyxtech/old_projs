# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, IPAddress

#ok
class Idc_typeForm(FlaskForm):
    id = HiddenField()
    desc = StringField(u'idc种类', validators=[Length(max=32)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class IdcForm(FlaskForm):
    id = HiddenField()
    name = StringField(u'机房名称', validators=[Length(max=100)])
    position = StringField(u'位置', validators=[Length(max=100)])
    idc_type_id = SelectField(u'机房类型信息', coerce=int)
    address = StringField(u'机房详细地址', validators=[Length(max=100)])
    serverCabinetNum = IntegerField(u'机柜数量')
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class CabinetForm(FlaskForm):
    id = HiddenField()
    designedpower = StringField(u'最大功率', validators=[Length(max=32)])
    idc_id = SelectField(u'机房', coerce=int)
    name = StringField(u'名称', validators=[Length(max=100)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class DeviceForm(FlaskForm):
    id = HiddenField()
  #  deviceType = SelectField(u'设备类型', coerce=int)
  #  deviceTypeId = SelectField(u'设备信息', coerce=int)
    serialNo = StringField(u'序列号', validators=[Length(max=64)])
    designedPower = StringField(u'功率', validators=[Length(max=64)])
    purchaseDate = DateField(u'购买日期')
    warrantyTime = DateField(u'保修时间')
    ip = StringField(u'ipv4 ip', validators=[IPAddress(ipv4=True)])
    ip2 = StringField(u'ipv4 ip2', validators=[IPAddress(ipv4=True)])
    position = StringField(u'位置', validators=[Length(max=32)])
    carbinet_id = SelectField(u'机柜', coerce=int)
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class ServerDeviceForm(FlaskForm):
    id = HiddenField()
    deviceType = HiddenField() #设备类型
    deviceTypeId = HiddenField() #设备信息
    serialNo = StringField(u'序列号', validators=[Length(max=64)])
    designedPower = StringField(u'功率', validators=[Length(max=64)])
    purchaseDate = DateField(u'购买日期')
    warrantyTime = DateField(u'保修时间')
    ip = StringField(u'ipv4 ip', validators=[IPAddress(ipv4=True)])
    ip2 = StringField(u'ipv4 ip2', validators=[IPAddress(ipv4=True)])
    position = StringField(u'位置', validators=[Length(max=32)])
    carbinet_id = SelectField(u'机柜', coerce=int)
    comment = StringField(u'备注', validators=[Length(max=1024)])
    business_id = SelectField(u'业务', coerce=int)
    serverType_id = SelectField(u'服务器类型', coerce=int)
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#todo
class ServerForm(FlaskForm):
    id = HiddenField()
    business_id = SelectField(u'业务', coerce=int)
    serverType_id = SelectField(u'服务器类型', coerce=int)
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class ServerTypeForm(FlaskForm):

    id = HiddenField()
    name = StringField(u'名称', validators=[Length(max=64)])
    memorySlotNum = IntegerField(u'内存插槽数量')
    memoryNum = IntegerField(u'内存数量')
    cpu_id = SelectField(u'cpu', coerce=int)
    cpunum = IntegerField(u'cpu数量')
    memorymodel_id = SelectField(u'内存', coerce=int)
    manufacturer = StringField(u'生产厂家', validators=[Length(max=100)])
    deviceTypeName = StringField(u'设备类型名称', validators=[Length(max=100)])
    diskNum = IntegerField(u'磁盘插槽数量')
    diskTypeAId = SelectField(u'磁盘类型A', coerce=int)
    diskTypeANum = IntegerField(u'磁盘类型A的数量')
    diskTypeBId = SelectField(u'磁盘类型B', coerce=int)
    diskTypeBNum = IntegerField(u'磁盘类型B数量')
    networkadaperAType = StringField(u'网卡A', validators=[Length(max=100)])
    networkadaperANum = IntegerField(u'网卡A数量')
    networkadaperBType = StringField(u'网卡B', validators=[Length(max=100)])
    networkadaperBNum = IntegerField(u'网卡B数量')
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#todel
class DeviceManufacturerForm(FlaskForm):
    id = HiddenField()
    manufacturer = StringField(u'厂家名称', validators=[Length(max=32)])
    devicename = StringField(u'设备型号', validators=[Length(max=32)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class CpuModelForm(FlaskForm):
    id = HiddenField()
    model = StringField(u'型号', validators=[Length(max=100)])
    frequency = StringField(u'频率', validators=[Length(max=32)])
    corenum = IntegerField(u'核心数量')
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class MemoryModelForm(FlaskForm):
    id = HiddenField()
    frequency = StringField(u'频率', validators=[Length(max=30)])
    memGen = StringField(u'内存代', validators=[Length(max=30)])
    size = StringField(u'总容量', validators=[Length(max=32)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class BusinessForm(FlaskForm):
    id = HiddenField()
    name = StringField(u'业务名称', validators=[Length(max=64)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')

#ok
class DiskForm(FlaskForm):
    id = HiddenField()
    size = StringField(u'磁盘容量大小', validators=[Length(max=32)])
    rpmSpeed = StringField(u'转速', validators=[Length(max=32)])
    storageType = StringField(u'存储类型', validators=[Length(max=32)])
    manufacturer = StringField(u'生产厂家', validators=[Length(max=100)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class SystemConfigInfoForm(FlaskForm):
    id = HiddenField()
    javaVer = StringField(u'java ver', validators=[Length(max=100)])
    ip = StringField(u'ip', validators=[IPAddress(ipv4=True)])
    saltid = StringField(u'saltid', validators=[Length(max=100)])
    macAddress = StringField(u'mac', validators=[Length(max=100)])
    systemUserList = StringField(u'用户表', validators=[Length(max=1024)])
    networkConfig = StringField(u'网路配置', validators=[Length(max=1024)])
    storageMount = StringField(u'磁盘挂载', validators=[Length(max=1024)])
    rcLocal = StringField(u'开机启动任务', validators=[Length(max=1024)])
    firewall = StringField(u'防火墙配置', validators=[Length(max=1024)])
    journalConfig = StringField(u'日志配置', validators=[Length(max=1024)])
    selinuxEnabled = StringField(u'selinux', validators=[Length(max=1024)])
    crontabList = StringField(u'crontab任务', validators=[Length(max=1024)])
    sshdVer = StringField(u'sshd版本', validators=[Length(max=1024)])
    portsOpened = StringField(u'开发端口', validators=[Length(max=1024)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class DepartmentForm(FlaskForm):
    id = HiddenField()
    name = StringField(u'名称', validators=[Length(max=1024)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class PatchHistoryForm(FlaskForm):
    id = HiddenField()
    patchName = StringField(u'补丁名称', validators=[Length(max=32)])
    patchDate = DateField(u'补丁日期')
    appName = StringField(u'程序', validators=[Length(max=32)])
    executor = StringField(u'执行人', validators=[Length(max=32)])
    departId = SelectField(u'部门', coerce=int)
    business_id = SelectField(u'业务', coerce=int)
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')


class BusinessInfoForm(FlaskForm):
    id = HiddenField()
    deployDir = StringField(u'部署目录位置', validators=[Length(max=1024)])
    serverId = SelectField(u'服务器', coerce=int)
    businessStart = DateField(u'业务起始时间')
    businessEnd = DateField(u'业务结束时间')
    businessName = StringField(u'业务名称(业务2类)', validators=[Length(max=64)])
    confDir = StringField(u'配置文件位置', validators=[Length(max=1024)])
    ports = StringField(u'使用端口', validators=[Length(max=1024)])
    keyApp = StringField(u'关键应用(包含版本信息)', validators=[Length(max=1024)])
    relevantPerson = StringField(u'业务联系人', validators=[Length(max=100)])
    comment = StringField(u'备注', validators=[Length(max=1024)])
    submit = SubmitField(u'提交')
