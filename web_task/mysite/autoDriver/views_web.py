from django.shortcuts import render
from . import models
import json

from django.http import HttpResponse
from . import utils
from . import driveArea
from . import param



def haveSuitVehicle(areaNum):
    res = models.vehicle_task.objects.filter( taskType =0, taskStatus=0 )
    # TODO: get the min distance from vehicle to passenger
    if len(res)>0 :
        return res[0].vid_id
    else:
        return 0
    pass

def allocTask( tid, areaNum ):
    carNum = haveSuitVehicle(areaNum)
    if carNum != 0:
        models.task_info.objects.filter(tid=tid).update(vid_id = carNum)
    pass


def callbackTask(request):
    if (request.method == 'POST'):
        value = json.loads(request.body)
        tid = value['tid']
        carNum =  value['carNum']
        taskType = value['taskType']
        taskStatus = value['taskStatus']
        path = value['path']
        estimateTime = value['estimateTime']
        odometry = value['odometry']

    v_res = models.vehicle_task.objects.filter(tid = tid)
    if len(v_res == 0):
        result = '{' + param.conformMsg.format(1, 1) + '}'
        return HttpResponse(result)
    else:
        models.vehicle_task.objects.filter(tid = tid).update(path=path,estimateTime=estimateTime,
                                                                     odometry=odometry)
    result = '{' + param.conformMsg.format(0, 1) + '}'
    return HttpResponse(result)