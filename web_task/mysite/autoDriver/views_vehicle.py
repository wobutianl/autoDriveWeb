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
        models.vehicle_info.objects.create(car_num=carNum, vehicle_type = vehicleType)
    else:   # have msg in task table or not
        res = models.vehicle_task.objects.filter( car_num_id = v_res[0].car_num )
        if len(res) > 0:
            if haveTask :
                models.vehicle_task.objects.filter( car_num_id = res[0].car_num).update(
                     lon=lon, lat=lat,available = available, battery=battery,
                    estimate_time=estimateTime, odometry=odometry , have_task = True)
            elif res[0].have_task == True:
                cur_time = datetime.now()
                if (cur_time - res[0].endTime).seconds > 120:
                    models.vehicle_task.objects.filter(car_num_id=res[0].car_num).update(
                        lon=lon, lat=lat, available=available, battery=battery, have_task = False )
                else:
                    models.vehicle_task.objects.filter(car_num_id=res[0].car_num).update(
                        lon=lon, lat=lat, available=available, battery=battery )
            else:
                models.vehicle_task.objects.filter(car_num_id=res[0].car_num).update(
                    lon=lon, lat=lat, available=available, battery=battery )
        else:
            models.vehicle_task.objects.create(car_num_id =v_res[0].car_num,
                                         lon=lon, lat=lat, available=available,
                                         battery=battery )

    result = '{' + param.conformMsg.format(1, 0) + '}'
    return HttpResponse(result)
    pass


# get the task : 1,1
def getTask(request, carNum, vehicleType):
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=1 )
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
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=2,
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
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=3)
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
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=4
                                                                    , endTime=datetime.now() )
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass