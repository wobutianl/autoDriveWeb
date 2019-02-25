from django.shortcuts import render
from . import models
import json

from django.http import HttpResponse
from . import utils
from . import driveArea
from . import param

def index2(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def updateApp(request, pid, lon, lat, tasktype, taskstatus):
    #try:
    res = models.app_task.objects.filter( pid_id = pid )
    if len(res) > 0:
        models.app_task.objects.filter( pid_id=pid ).update(taskType=tasktype, taskStatus=taskstatus,
                                                                     lon=lon, lat=lat)
        updateTaskInfo(res[0].tid)
    else:
        models.app_task.objects.create(pid_id = pid, taskType = tasktype, taskStatus = taskstatus,
                                                       lon = lon, lat = lat)

    result = '{' + param.conformMsg.format(0, 0) + '}'
    return HttpResponse(result)
    # except :
    #     result = '{' + param.conformMsg.format(0, 2) + '}'
    #     return HttpResponse( result)
    pass

def updateVehicle(request):
    if (request.method == 'POST'):
        value = json.loads(request.body)
        carNum = value['carNum']
        available = value['available']
        taskType = value['taskType']
        taskStatus = value['taskStatus']
        vehicleType = value['vehicleType']
        lon = value['lon']
        lat = value['lat']
        battery = value['battery']
        velocity = value['velocity']
        direction = value['direction']
        estimateTime = value['estimateTime']
        odometry = value['odometry']

    v_res = models.vehicle_info.objects.filter( carNum = carNum)
    if len(v_res==0):
        models.vehicle_info.objects.create(carNum=carNum, vehicleType = vehicleType)

    else:
        res = models.vehicle_task.objects.filter( vid_id = v_res[0].vid)
        if len(res) > 0:
            # web allocate task
            t_res = models.task_info.objects.filter(vid_id=v_res[0].vid, beSured = False)
            if len(t_res)>0 and res[0].taskType == 0 and res[0].taskStatus == 0:
                result = param.webToVehicle.format(t_res[0].tid, 1, 0, t_res[0].startlat, t_res[0].startlon)
                return HttpResponse( result)

            # vehicle get task  / change task info
            t_res = models.task_info.objects.filter(vid_id=v_res[0].vid, beSured=False)
            if len(t_res) > 0 and res[0].taskType == 1 and res[0].taskStatus == 1:
                models.task_info.objects.filter(tid = t_res[0].tid).update(taskType = 1, taskStatus=1, beSured=True)

            # t_res = models.task_info.objects.filter(vid_id=v_res[0].vid, beSured=False)
            if len(t_res) > 0 and res[0].taskType == 2 and res[0].taskStatus == 1:
                models.task_info.objects.filter(tid = t_res[0].tid, beSured=True).update(taskType = 2, taskStatus=1)

            models.vehicle_task.objects.filter( vid_id = res[0].vid).update(taskType=taskType, taskStatus=taskStatus,
                     lon=lon, lat=lat,available = available, battery=battery,velocity = velocity,
                    direction = direction, estimateTime=estimateTime, odometry=odometry )
            updateTaskInfo( res[0].tid )
        else:
            models.vehicle_task.objects.create(vid_id =v_res[0].vid, taskType=taskType, taskStatus=taskStatus,
                                         lon=lon, lat=lat, available=available,
                                         battery=battery, velocity=velocity,
                                         direction=direction, estimateTime=estimateTime,
                                         odometry=odometry)

    result = '{' + param.conformMsg.format(1, 0) + '}'
    return HttpResponse(result)
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
        models.vehicle_task.objects.filter(tid = tid).update(taskType=taskType, taskStatus=taskStatus,
                                                                     path=path,estimateTime=estimateTime,
                                                                     odometry=odometry)
    result = '{' + param.conformMsg.format(0, 1) + '}'
    return HttpResponse(result)

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

def updateTaskInfo(tid):
    # get app task
    # get vehicle task
    t_res = models.task_info.objects.filter(tid = tid)
    if len(t_res)>0:
        app_res = models.app_task.objects.filter(pid_id=t_res[0].pid_id)
        v_res = models.vehicle_task.objects.filter(vid_id=t_res[0].vid_id)
        if t_res[0].current_task == False:  # msg from not current task vehicle
            models.task_info.objects.filter( tid=tid ).update(
                taskType=v_res[0].taskType, taskStatus=v_res[0].taskStatus)
        if len(app_res)>0 and len(v_res)>0:
            if app_res[0].taskType == 2 and app_res[0].taskStatus == 3:
                models.task_info.objects.filter( tid=tid ).update( endStatus=1 )
                other_task_res = models.task_info.objects.filter( pid_id = t_res[0].pid_id, endStatus=0, current_task=False)
                if len(other_task_res) > 0:  # have other task
                    models.task_info.objects.filter(tid=other_task_res[0].tid).update(  current_task=True )
                else:
                    models.task_info.objects.filter(tid=tid).update( endStatus = 1)
            else: # just have one task
                status = utils.getTaskStatus(app_res[0].taskType, app_res[0].taskStatus,
                                    v_res[0].taskType, v_res[0].taskStatus)
                models.task_info.objects.filter(tid=tid).update(
                    taskType=status[0], taskStatus=status[1])
    pass

def startTask(request, pid, startlon, startlat, endlon, endlat):
    '''
    same area:  
    several area:
    inWhichArea(startlon, startlat)
    bDiffArea = False
    '''
    startArea = utils.inWhichArea(startlat, startlon)
    endArea = utils.inWhichArea(endlat, endlon)
    if startArea == 0 or endArea == 0 :
        result = '{' + param.conformMsg.format(0, 1) + '}'
        return HttpResponse(result)
    elif startArea == endArea:
        # insert into task_info
        try :
            models.task_info.objects.create(pid_id=pid, startlon = startlon, startlat = startlat,
                                            endlon = endlon, endlat = endlat, taskType = 1,
                                            taskStatus = 0)
            result = '{' + param.conformMsg.format(0, 0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format(0, 1) + '}'
            return HttpResponse(result)
    else:
        dockNum = utils.chooseDock(startlat , startlon, startArea)
        transferPoints = [ driveArea.dockPoint[startArea-1][dockNum] ]
        midLat = driveArea.dockPoint[startArea-1][dockNum].x
        midLon = driveArea.dockPoint[startArea-1][dockNum].y
        try :
            models.task_info.objects.create(pid_id=pid, startlon = startlon, startlat = startlat,
                                            endlon = midLon, endlat = midLat, taskType = 1,
                                            taskStatus = 0, transferPoints = transferPoints,
                                            current_task = True, isCombineTask = True)
            models.task_info.objects.create(pid_id=pid, startlon=midLon, startlat=midLat,
                                            endlon=endlon, endlat=endlat, taskType=1,
                                            taskStatus=0, transferPoints=transferPoints,
                                            current_task=False, isCombineTask = True)
            result = '{' + param.conformMsg.format(0, 0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format(0, 1) + '}'
            return HttpResponse(result)
    pass

def goTask(request, pid):
    # try:
    res = models.task_info.objects.filter(pid_id = pid, current_task = True)
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(0, 1) + '}'
        return HttpResponse(result)
    for row in res:
        if row.taskType == 1 and row.taskStatus == 3:
            models.task_info.objects.filter(pid_id=pid, current_task=True).update(taskType=2, taskStatus=0)
            result = '{' + param.conformMsg.format(0, 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format(0, 1) + '}'
            return HttpResponse(result)
    pass

def parkTask(request, pid, carNum):
    pass

def launchTask(request, pid, carNum):
    pass

def cancelTask(request, pid):
    print(pid )
    string  = "he {}".format( pid )
    return HttpResponse(string)
    pass

def registerTask(request, pid, password):
    try:
        # print(pid, password)
        models.app_info.objects.create( pid = pid, pwd = password)
        result = '{' + param.conformMsg.format(0, 0) + '}'
        return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(0,1 ) + '}'
        return HttpResponse( result)

    pass

def loginTask(request, pid, password):
    try:
        res = models.app_info.objects.filter( pid = pid, pwd = password)
        if len(res) > 0:
            result = '{' + param.conformMsg.format(0, 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format(0, 1) + '}'
            return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(0, 2) + '}'
        return HttpResponse( result)
    pass

def parkInfo(request, pid):
    pass

def unstartInfo(request, pid):
    pass

def vehicleInfo(request, pid, carNum):
    pass

def vehicleIdInfo(request, pid):
    pass

def comformMsg(request, pid):
    pass