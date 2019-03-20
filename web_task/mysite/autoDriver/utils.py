# -*- coding: utf-8
from shapely.geometry import Polygon, Point
from . import driveArea
from datetime import datetime
import math 

def inWhichArea( lat, lon ):
    p = Point(lon, lat)
    # print (p)
    if p.within(driveArea.areaA):
        print(1)
        return 1
    elif p.within(driveArea.areaB):
        print(2)
        return 2
    else:
        return 0
    pass

def chooseDock( lat, lon, areaNum):
    # just care about the distance from begin point to dock
    sp = Point(lat, lon)
    if areaNum == 1:
        points = driveArea.dockPoint[0]
    elif areaNum == 2:
        points = driveArea.dockPoint[1]
    min_distance = 0.0
    dock_num = -1
    for p in points:
        i = 0
        d = sp.distance(p)
        if min_distance > d:
            dock_num = i
        i = i+1
    return dock_num


def getTaskStatus(app_taskType, app_taskStatus, v_taskType, v_taskStatus):
    taskType = 0
    taskStatus = 0
    if app_taskType > v_taskType:
        taskType = app_taskType
    elif app_taskType == v_taskType:
        if app_taskStatus >= v_taskStatus :
            taskStatus = app_taskStatus
        elif app_taskStatus < v_taskStatus:
            taskStatus = v_taskStatus
    return (taskType, taskStatus)
    pass


def str2datetime(dateTime):
    return datetime.strptime( dateTime ,"%Y-%m-%d %H:%M:%S.%f")

a = 6378245.0 # 克拉索夫斯基椭球参数长半轴a
ee = 0.00669342162296594323 #克拉索夫斯基椭球参数第一偏心率平方
PI = 3.14159265358979324 # 圆周率

def gcj2wgs(lon, lat):
    # 以下为转换公式 
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    #纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return (wgsLon,wgsLat )




def wgs2gcj(lon, lat):

    dLat = transform_lat(lon - 105.0, lat - 35.0)
    dLon = transform_lon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return (mgLon, mgLat)


def transform_lat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret


def transform_lon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret