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
def update(request, carNum, vehicleType, available, lon, lat, haveTask, battery, estimateTime, odometry):
    v_res = models.vehicle_info.objects.filter( car_num = carNum, vehicle_type=vehicleType)
    if len(v_res) == 0: # register in db
        models.vehicle_info.objects.create(car_num=carNum, vehicle_type = vehicleType,lon=lon, lat=lat,available = available, battery=battery,
                    estimate_time=estimateTime, odometry=odometry , have_task = False, end_time = '0' )
    else:   # have msg in task table or not
        if haveTask :
            models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat,available = available, battery=battery,
                estimate_time=estimateTime, odometry=odometry , have_task = True)
        elif v_res[0].have_task == True:
            cur_time = datetime.now()
            if (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds > 120:
                models.vehicle_info.objects.filter(car_num=carNum).update(
                    lon=lon, lat=lat, available=available, battery=battery, 
                    estimate_time=0.0, odometry=0.0 ,have_task = False )
            else:
                models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat, available=available, battery=battery, estimate_time=0.0, odometry=0.0  )
        else:
            models.vehicle_info.objects.filter( car_num=carNum ).update(
                lon=lon, lat=lat, available=available, battery=battery , estimate_time=0.0, odometry=0.0 )

    result = '{' + param.conformMsg.format(1, 0) + '}'
    return HttpResponse(result)
    pass


# get the task : 1,1
def getTask(request, carNum, vehicleType):
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(task_type=1, task_status=1 )
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def begin(request, carNum, vehicleType):
    if (request.method == 'POST'):
        value = json.loads(request.body)
        if isinstance(value, dict):
            path = value['path']
            estimateTime = value['estimateTime']
            odometry = value['odometry']

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(task_type=1, task_status=2,
                                  path=path, estimate_time=estimateTime, odometry=odometry)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def run(request, carNum, vehicleType):
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(task_type=1, task_status=3)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def arrival(request, carNum, vehicleType):
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(task_type=1, task_status=4
                                                                    , end_time=str(datetime.now()) )
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass