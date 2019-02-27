from django.shortcuts import render
from . import models
import json

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
def update(request, carNum, result):
    if (request.method == 'POST'):
        value = json.loads(request.body)
        haveTask = False
        haveSensor = False
        # carNum = value['carNum']
        if isinstance(value, dict):
            for key in value:
                if key == "basic":
                    if isinstance(value[key], dict):
                        available = value['available']
                        vehicleType = value['vehicleType']
                        lon = value['lon']
                        lat = value['lat']
                        battery = value['battery']
                        velocity = value['velocity']
                elif key == "havetask":
                    if isinstance(value[key], dict):
                        haveTask = True
                        direction = value['direction']
                        estimateTime = value['estimateTime']
                        odometry = value['odometry']
                elif key == "sensor":
                    if isinstance(value[key], dict):
                        haveSensor = True
                        camera = value['camera']
                        lidar = value['lidar']
                        radar = value['radar']
                        rtk = value['rtk']
                        px2 = value['px2']
                        ipc = value['ipc']

    v_res = models.vehicle_info.objects.filter( carNum = carNum)
    if len(v_res==0): # register in db
        models.vehicle_info.objects.create(carNum=carNum, vehicleType = vehicleType)
    else:   # have msg in task table or not
        res = models.vehicle_task.objects.filter( vid_id = v_res[0].vid)
        if len(res) > 0:
            if haveTask :
                models.vehicle_task.objects.filter( vid_id = res[0].vid).update(
                     lon=lon, lat=lat,available = available, battery=battery,velocity = velocity,
                    direction = direction, estimateTime=estimateTime, odometry=odometry )
            else:
                models.vehicle_task.objects.filter(vid_id=res[0].vid).update(
                    lon=lon, lat=lat, available=available, battery=battery )
                # if vid have task in task table
                # send task to vehicle
        else:
            models.vehicle_task.objects.create(vid_id =v_res[0].vid,
                                         lon=lon, lat=lat, available=available,
                                         battery=battery )

    result = '{' + param.conformMsg.format(1, 0) + '}'
    return HttpResponse(result)
    pass


# get the task : 1,1
def getTask(request, carNum, result):
    v_res = models.vehicle_info.objects.filter(carNum=carNum)
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

def begin(request, carNum, result):
    if (request.method == 'POST'):
        value = json.loads(request.body)
        if isinstance(value, dict):
            path = value['path']
            estimateTime = value['estimateTime']
            odometry = value['odometry']

    v_res = models.vehicle_info.objects.filter(carNum=carNum)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=2,
                                  path=path, estimateTime=estimateTime, odometry=odometry)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

def run(request, carNum, result):
    v_res = models.vehicle_info.objects.filter(carNum=carNum)
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

def arrival(request, carNum, result):
    v_res = models.vehicle_info.objects.filter(carNum=carNum)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(vid_id=v_res[0].vid).update(taskType=1, taskStatus=4)
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass