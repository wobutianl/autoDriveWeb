from django.shortcuts import render
from . import models
import json


import time 
from datetime import datetime 

from django.http import HttpResponse
from . import utils
from . import driveArea
from . import param
from . import views_web

'''
for basic : exists all the time
for task : when there have a task 
for sensor : when sensor changed 
'''
def update(request):
    if request.method == 'GET':
        carNum = request.GET.get('vid',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')
        available = request.GET.get('available', default='1')
        lon = request.GET.get('lon', default='0')
        lat = request.GET.get('lat', default='0')

        haveTask = request.GET.get('haveTask', default='0')
        battery = request.GET.get('battery',default='0')
        estimateTime = request.GET.get('estimateTime', default='0')
        odometry = request.GET.get('odometry', default='1')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    
    v_res = models.vehicle_info.objects.filter( car_num = carNum, vehicle_type=vehicleType)
    if len(v_res) == 0: # register in db
        models.vehicle_info.objects.create(car_num=carNum, vehicle_type = vehicleType,lon=lon, lat=lat,available = available, battery=battery,
                    estimate_time=estimateTime, odometry=odometry , have_task = 0, end_time = '0' )
    else:   # have msg in task table or not
        if haveTask :
            models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat,available = available, battery=battery,
                estimate_time=estimateTime, odometry=odometry , have_task = 1)
        elif v_res[0].have_task == True:
            cur_time = datetime.now()
            if (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds > 120:
                models.vehicle_info.objects.filter(car_num=carNum).update(
                    lon=lon, lat=lat, available=available, battery=battery, 
                    estimate_time=0.0, odometry=0.0 ,have_task = 0 )
            else:
                models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat, available=available, battery=battery, estimate_time=0.0, odometry=0.0  )
        else:
            res = models.task_info.objects.filter( car_num = carNum, end_status=0, task_type=1, task_status=0)
            if len(res)>0:
                result = {'taskType = 1 :  lon': res[0].start_lon, 'lat': res[0].start_lat}
                return HttpResponse(result)
            res = models.task_info.objects.filter(car_num=carNum, end_status=0, task_type=2, task_status=0)
            if len(res) > 0:
                result = {'taskType = 2: lon': res[0].end_lon, 'lat': res[0].end_lat}
                return HttpResponse(result)

            models.vehicle_info.objects.filter( car_num=carNum ).update(
                lon=lon, lat=lat, available=available, battery=battery , estimate_time=0.0, odometry=0.0 )

    result = '{' + param.conformMsg.format( 0) + '}'
    return HttpResponse(result)
    pass

# get the task : 1,1
def getTask(request):
    if request.method == 'GET':
        carNum = request.GET.get('vid',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(car_num = carNum).update(task_type=1, task_status=1 )
        models.vehicle_info.objects.filter(car_num = carNum).update( have_task = 1 )
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def begin(request):
    if request.method == 'GET':
        carNum = request.GET.get('vid',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    if (request.method == 'POST'):
        value = json.loads(request.body)
        if isinstance(value, dict):
            path = value['path']
            estimateTime = value['estimateTime']
            odometry = value['odometry']

    path = [(121.1,31,2),(121.3, 31.2),(121.4,31,4)]
    estimateTime = 5
    odometry = 6
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(car_num=carNum).update(task_type=1, task_status=2,
                                  path=path)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    result = '{' + param.conformMsg.format(1) + '}'
    return HttpResponse(result)

def run(request):
    if request.method == 'GET':
        carNum = request.GET.get('vid',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(car_num=carNum).update(task_type=1, task_status=3)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def arrival(request):
    if request.method == 'GET':
        carNum = request.GET.get('vid',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(car_num=carNum).update( task_status=4 )
        res = models.task_info.objects.filter(car_num=carNum, task_type=2)
        if len(res)>0:
            models.vehicle_info.objects.filter(car_num=carNum).update(end_time=str(datetime.now()))
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass