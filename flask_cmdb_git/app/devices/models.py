# encoding: utf-8
from app import db

#ok
class Idc_type(db.Model):
    __tablename__ = 'Idc_type'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(32))  # idc种类
    comment = db.Column(db.String(1024))  # 备注

#ok
class Idc(db.Model):
    __tablename__ = 'Idc'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100))  # 位置
    idc_type_id = db.Column(db.Integer, db.ForeignKey('Idc_type.id'))  # 机房类型信息
    address = db.Column(db.String(100))  # 机房详细地址
    serverCabinetNum = db.Column(db.Integer)  # 机柜数量
    name = db.Column(db.String(100))  # 机房名称
    comment = db.Column(db.String(1024))  # 备注

#ok
class Cabinet(db.Model):
    __tablename__ = 'Cabinet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 名称
    designedpower = db.Column(db.String(32))  # 最大功率
    idc = db.Column(db.Integer, db.ForeignKey('Idc.id'))  # 机房
    comment = db.Column(db.String(1024))  # 备注

#todo
class Device(db.Model):
    __tablename__ = 'Device'
    id = db.Column(db.Integer, primary_key=True)
    deviceType = db.Column(db.Integer)  # 设备类型 ，1服务器，2网络设备，3安全设备
    deviceTypeId = db.Column(db.Integer)  # 设备id
    serialNo = db.Column(db.String(64))  # 序列号
    designedPower = db.Column(db.String(64))  # 功率
    purchaseDate = db.Column(db.DateTime)  # 购买日期
    warrantyTime = db.Column(db.DateTime)  # 保修时间
    ip = db.Column(db.String(64))  # ipv4 ip
    ip2 = db.Column(db.String(64))  # ipv4 ip2
    position = db.Column(db.String(32))  # 位置
    carbinet_id = db.Column(db.Integer, db.ForeignKey('Cabinet.id'))  # 机柜
    comment = db.Column(db.String(1024))  # 注释

#todo
class Server(db.Model):
    __tablename__ = 'Server'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('Business.id'))  # 业务id
    serverType_id = db.Column(db.Integer, db.ForeignKey('ServerType.id'))  # 服务器类型
    comment = db.Column(db.String(1024))  # 注释


class ServerType(db.Model):
    __tablename__ = 'ServerType'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))  # 设备类型名称
    memorySlotNum = db.Column(db.Integer)  # 内存插槽数量
    memoryNum = db.Column(db.Integer)  # 内存数量
    cpunum = db.Column(db.Integer)  # cpu数量
    cpu_id = db.Column(db.Integer, db.ForeignKey('CpuModel.id'))  # cpu type id
    memorymodel_id = db.Column(db.Integer, db.ForeignKey('MemoryModel.id'))  # 内存型号
    manufacturer = db.Column(db.String(100))  # 生产厂家
    deviceTypeName = db.Column(db.String(100))  # 型号名称
    diskNum = db.Column(db.Integer)  # 磁盘插槽数量
    diskTypeAId = db.Column(db.Integer)  # 磁盘类型A的数量
    diskTypeANum = db.Column(db.Integer)  # 磁盘类型A的id
    diskTypeBId = db.Column(db.Integer)  # 磁盘类型B的id
    diskTypeBNum = db.Column(db.Integer)  # 磁盘类型B数量
    networkadaperAType = db.Column(db.String(100))  # 网卡A
    networkadaperANum = db.Column(db.Integer)  # 网卡A数量
    networkadaperBType = db.Column(db.String(100))  # 网卡B
    networkadaperBNum = db.Column(db.Integer)  # 网卡B数量
    comment = db.Column(db.String(1024))  # 备注

#todel
class DeviceManufacturer(db.Model):
    __tablename__ = 'DeviceManufacturer'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(32))  # 生产厂商
    devicename = db.Column(db.String(32))  # 设备型号
    comment = db.Column(db.String(1024))  # 备注

#ok
class CpuModel(db.Model):
    __tablename__ = 'CpuModel'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100))  # 型号
    frequency = db.Column(db.String(32))  # 频率
    corenum = db.Column(db.Integer)  # 核心数量
    comment = db.Column(db.String(1024))  # 备注

#ok
class MemoryModel(db.Model):
    __tablename__ = 'MemoryModel'
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(30))  # 频率
    memGen = db.Column(db.String(30))  # 内存代
    size = db.Column(db.String(32))  # 总容量
    comment = db.Column(db.String(1024))  # 备注

#ok
class Business(db.Model):
    __tablename__ = 'Business'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))  # 业务名称
    comment = db.Column(db.String(1024))  # 注释

#OK
class Disk(db.Model):
    __tablename__ = 'Disk'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(32))  # 磁盘容量大小
    rpmSpeed = db.Column(db.String(32))  # 转速
    storageType = db.Column(db.String(32))  # 存储类型
    manufacturer = db.Column(db.String(100))  # 生产厂家
    comment = db.Column(db.String(1024))  # 注释


class SystemConfigInfo(db.Model):
    __tablename__ = 'SystemConfigInfo'
    id = db.Column(db.Integer, primary_key=True)
    javaVer = db.Column(db.String(100))  # java ver
    ip = db.Column(db.String(100))  # IP
    saltid = db.Column(db.String(100))  # saltid
    macAddress = db.Column(db.String(100))  # mac
    systemUserList = db.Column(db.String(1024))  # 用户表
    networkConfig = db.Column(db.String(1024))  # 网路配置
    storageMount = db.Column(db.String(1024))  # 磁盘挂载
    rcLocal = db.Column(db.String(1024))  # 开机启动任务
    firewall = db.Column(db.String(1024))  # 防火墙配置
    journalConfig = db.Column(db.String(1024))  # 日志配置
    selinuxEnabled = db.Column(db.String(100))  # selinux
    crontabList = db.Column(db.String(1024))  # crontab任务
    sshdVer = db.Column(db.String(100))  # sshd版本
    portsOpened = db.Column(db.String(1024))  #开发端口
    comment = db.Column(db.String(1024))  # 注释



##no cleared


class NetworkDeviceModel(db.Model):
    __tablename__ = 'NetworkDeviceModel'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100))  # 生产厂家
    devicename = db.Column(db.String(100))  # 名称
    comment = db.Column(db.String(1024))  # 备注


class SecurityDeviceModel(db.Model):
    __tablename__ = 'SecurityDeviceModel'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100))  # 生产厂家
    devicename = db.Column(db.String(100))  # 名称
    comment = db.Column(db.String(1024))  # 备注


class SecurityDevice(db.Model):
    __tablename__ = 'SecurityDevice'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(32))  # 位置
    devicetype = db.Column(db.Integer)  # 设备型号
    serialno = db.Column(db.String(32))  # 序列号
    designedpower = db.Column(db.String(32))  # 功率
    purchasedate = db.Column(db.DateTime)  # 购买日期
    warrantytime = db.Column(db.String(32))  # 保修时间
    traffic = db.Column(db.String(32))  # 流量
    crydecspeed = db.Column(db.String(32))  # 加解密速度
    portnum = db.Column(db.Integer)  # 端口数量
    comment = db.Column(db.String(1024))  # 备注


class NetworkDevice(db.Model):
    __tablename__ = 'NetworkDevice'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(32))  # 位置
    devicetype = db.Column(db.Integer)  # 设备型号
    serialno = db.Column(db.String(32))  # 序列号
    designedpower = db.Column(db.String(32))  # 功率
    purchasedate = db.Column(db.DateTime)  # 购买日期
    warrantytime = db.Column(db.DateTime)  # 保修时间
    normalport = db.Column(db.Integer)  # 普通网口数量
    opticalport = db.Column(db.Integer)  # 光口数量
    traffic = db.Column(db.String(32))  # 流量
    opticalmodel = db.Column(db.String(1024))  # 光模块
    comment = db.Column(db.String(1024))  # 备注


class Department(db.Model):
    __tablename__ = 'Department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))  # 名称
    comment = db.Column(db.String(1024))  # 备注


class PatchHistory(db.Model):
    __tablename__ = 'PatchHistory'
    id = db.Column(db.Integer, primary_key=True)
    patchName = db.Column(db.String(32))  # 补丁名称
    patchDate = db.Column(db.DateTime)  # 补丁日期
    appName = db.Column(db.String(32))  # 程序
    executor = db.Column(db.String(32))  # 执行人
    departId = db.Column(db.Integer, db.ForeignKey("Department.id"))  # 部门
    business_id = db.Column(db.Integer, db.ForeignKey('Business.id'))  # 业务
    comment = db.Column(db.String(1024))  # 备注


# 业务(自动采集+手动填写)
class BusinessInfo(db.Model):
    __tablename__ = 'BusinessInfo'
    id = db.Column(db.Integer, primary_key=True)
    deployDir = db.Column(db.String(1024))  # 部署目录位置
    serverId = db.Column(db.Integer, db.ForeignKey("Device.id"))  # 服务器id
    businessStart = db.Column(db.DateTime)  # 业务起始时间
    businessEnd = db.Column(db.DateTime)  # 业务结束时间
    businessName = db.Column(db.String(64))  # 业务名称(业务2类)
    confDir = db.Column(db.String(1024))  # 配置文件位置
    ports = db.Column(db.String(1024))  # 使用端口
    keyApp = db.Column(db.String(1024))  # 关键应用(包含版本信息)
    relevantPerson = db.Column(db.String(100))  # 业务联系人
    comment = db.Column(db.String(1024))  # 备注
    parentBusinessId = db.Column(db.INTEGER, db.ForeignKey('Business.id'))














