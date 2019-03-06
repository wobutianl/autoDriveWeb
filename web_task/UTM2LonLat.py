# -*- coding: utf-8 -*-

import os 
import math 



'''
file_path = r"D:\document\autoDriveWeb\map_data\small_circuit.txt"
output_path = r"D:\document\autoDriveWeb\map_data\small_lonlat.txt"

def utm_lonlat(utmx, utmy):
    x = utmx/20037508.34*180 + 31.816895
    y = utmy/20037508.34*180 + 120.013454
    #y = 180/math.pi *(2* math.atan (math.exp(y* math.pi/180))- math.pi/2)
    print ( x, y )
    return (x, y)


with open(file_path, 'r') as f :
    with open(output_path, 'w') as wf:
        for line in f.readlines():
            point = line.split(' ')
            v1 = utm_lonlat( float(point[0]), float(point[1]) )
            wf.write('(' + str(v1[0]) + ',' + str(v1[1]) + '),' )

'''


"""
Created on Wed Jan 24 17:00:23 2018

@author: liuj
"""
import json 
from urllib.request import urlopen 
from pyproj import Proj 

p = Proj(datum= 'NAD83',proj='utm',zone=51,ellps='GRS80',units='m') 
xmin,ymin=p(113.192658,23.047543) #左下角
xmax,ymax=p(113.403306,23.170221) #右上角

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率



def UTMtoGeog(x,y):#平面坐标转WGS84坐标系
    k0=0.9996
    a=6378137
    f=1/298.257222101
    b = a*(1-f) 
    e = math.sqrt(1 - (b/a)*(b/a)) 
    esq = (1 - (b/a)*(b/a)) 
    e0sq = e*e/(1-e*e) 
    zone=51
    zcm = 3 + 6*(zone-1) - 180
    e1 = (1 - math.sqrt(1 - e*e))/(1 + math.sqrt(1 - e*e)) 
    M0 = 0
    M = M0 + y/k0 
    mu = M/(a*(1 - esq*(1/4 + esq*(3/64 + 5*esq/256)))) 
    phi1 = mu + e1*(3/2 - 27*e1*e1/32)*math.sin(2*mu) + e1*e1*(21/16 -55*e1*e1/32)*math.sin(4*mu) 
    phi1 = phi1 + e1*e1*e1*(math.sin(6*mu)*151/96 + e1*math.sin(8*mu)*1097/512) 
    C1 = e0sq*math.pow(math.cos(phi1),2) 
    T1 = math.pow(math.tan(phi1),2) 
    N1 = a/math.sqrt(1-math.pow(e*math.sin(phi1),2)) 
    R1 = N1*(1-e*e)/(1-math.pow(e*math.sin(phi1),2)) 
    D = (x-500000)/(N1*k0) 
    phi = (D*D)*(1/2 - D*D*(5 + 3*T1 + 10*C1 - 4*C1*C1 - 9*e0sq)/24) 
    phi = phi + math.pow(D,6)*(61 + 90*T1 + 298*C1 + 45*T1*T1 -252*e0sq - 3*C1*C1)/720
    phi = phi1 - (N1*math.tan(phi1)/R1)*phi 
    lng = D*(1 + D*D*((-1 -2*T1 -C1)/6 + D*D*(5 - 2*C1 + 28*T1 - 3*C1*C1 +8*e0sq + 24*T1*T1)/120))/math.cos(phi1) 
    drad=math.pi/180
    lngd = zcm+lng/drad 
    latd=phi/drad+0.0000001
    xd=math.floor(10000000*lngd)/10000000
    yd=math.floor(10000000*latd)/10000000
    return xd,yd 

def newtoold(x,y):#像素坐标转平面坐标
    xmin,xmax=(708040.22626217513, 788040.22626217513) 
    ymin,ymax=(2417700.9535092441, 2497700.9535092441) 
    scalex=(xmax-xmin)/18480
    scaley=(ymax-ymin)/18480
    x_old=x*scalex+xmin 
    y_old=ymax-y*scaley 
    return x_old,y_old 

def getlnglat(o_lon,o_lat):#将wgs84坐标转为百度经纬度坐标，from 1 to 5
    uri = 'http://api.map.baidu.com/geoconv/v1/?coords='
    ak = 'YMbDVTPOYihm2uEfS6j1DtZhLCOsGcnV'
    url = uri+str(o_lon)+','+str(o_lat)+'&from=1&to=5&ak='+ak 
    req = urlopen(url) 
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    return temp 
def transform_lng(lng, lat): 
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng)) 
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 * math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 * math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret 

def transform_lat(lng, lat): 
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng)) 
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 * math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret 
    
def out_of_china(lng, lat): 
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    #return False
    return not (135.05 > lng  > 73.66  and  53.55> lat > 3.86 ) 
    
def wgs84_to_gcj02(lng, lat): 
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 扁率
    if out_of_china(lng, lat): # 判断是否在国内
        return lng, lat 
        
    dlat = transform_lat(lng - 105.0, lat - 35.0) 
    dlng = transform_lng(lng - 105.0, lat - 35.0) 
    radlat = lat / 180.0 * math.pi 
    magic = math.sin(radlat) 
    magic = 1 - ee * magic * magic 
    sqrtmagic = math.sqrt(magic) 
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi) 
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi) 
    mglat = lat + dlat 
    mglng = lng + dlng 
    return [mglng, mglat] 
    
def bd09_to_gcj02(bd_lon, bd_lat): 
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi) 
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi) 
    gg_lng = z * math.cos(theta) 
    gg_lat = z * math.sin(theta) 
    return [gg_lng, gg_lat] 
    
def gcj02_to_wgs84(lng, lat): 
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat): 
        return lng, lat 
        
    dlat = transform_lat(lng - 105.0, lat - 35.0) 
    dlng = transform_lng(lng - 105.0, lat - 35.0) 
    radlat = lat / 180.0 * pi 
    magic = math.sin(radlat) 
    magic = 1 - ee * magic * magic 
    sqrtmagic = math.sqrt(magic) 
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi) 
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi) 
    mglat = lat + dlat 
    mglng = lng + dlng 
    return [lng * 2 - mglng, lat * 2 - mglat] 
    
def gcj02_to_bd09(lng, lat): 
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi) 
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi) 
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat] 
    
def bd09_to_wgs84(bd_lon, bd_lat): 
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat) 
    return gcj02_to_wgs84(lon, lat) 
    
def wgs84_to_bd09(lon, lat): 
    lon, lat = wgs84_to_gcj02(lon, lat) 
    return gcj02_to_bd09(lon, lat) 
    
def utm_lonlat_file(utm_file, lonlat_file):
    with open(file_path, 'r') as f :
        with open(output_path, 'w') as wf:
            for line in f.readlines():
                point = line.split(' ')
                v1 = UTMtoGeog( float(point[0]), float(point[1]) )
                wf.write('(' + str(v1[1]) + ',' + str(v1[0]) + '),' )

def kml_format(kml_file, format_file):
    
    with open(file_path, 'r') as f :
        with open(output_path, 'w') as wf:
            for line in f.readlines():
                point = line.split(' ')
                print ('a', point) 
                #for i in range(0, len(point) - 3, 3):
                for i in point:
                    k = i.split(',')
                    wf.write('(' + str(k[1]) + ',' + str(k[0]) + '),' )

if __name__ == "__main__":
    # file_path = r"D:\document\autoDriveWeb\map_data\big_circle.txt"
    # output_path = r"D:\document\autoDriveWeb\map_data\big_lonlat.txt"
    # kml_format(file_path, output_path)

    file_path = r"D:\document\autoDriveWeb\map_data\small_circuit.txt"
    output_path = r"D:\document\autoDriveWeb\map_data\small_lonlat.txt"
    utm_lonlat_file(file_path, output_path)
    


'''
    s = "367264.97961555282 3451304.3413151186"
    res = ''
    coord = s.split(" ")
    lnt = coord[0] 
    lat = coord[1] 
    coord = UTMtoGeog(float(lnt), float(lat)) #lnt = str(coord[0])
    #lat = str(coord[1])
    #print(type(lnt))
    res = res + str(coord[0]) + "," + str(coord[1]) + ";"
    print(res)

'''