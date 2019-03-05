from django.shortcuts import render
from . import models
import json

from django.http import HttpResponse
from . import utils
from . import driveArea
from . import param
from . import views_web

def index2(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#########################    APP  interface  ##############################################

# just update lon lat and make sure app get the msg
def update(request, pid, lon, lat, tasktype, taskstatus):
    #try:
    res = models.app_task.objects.filter( pid_id = pid )
    # to know whether the pid have task all in able
    if len(res) > 0:
        models.app_task.objects.filter( pid_id=pid ).update(lon=lon, lat=lat)
        '''
        have task : 
            get 1,0, check car getTask, if get return 1,1 else return 0
            get 1,1, check car prepared , return 1,2 and taskList
            get 1,2, check car status , return 1, 3
            get 1,3, check car status ,
            get 1,4, return 0
            get 2,0, check car getTask, if get return 1,1 else return 0
            get 2,4, (one task : then change task status)
                     (two task : change two of the task )
        ''' 
        if tasktype == 1 and taskstatus == 0:
            res = models.task_info.objects.filter( pid_id = pid, endStatus=0, taskStatus=0 )
            if len(res) > 0 :
                result = '{' + param.conformMsg.format( 0) + '}'
            else :
                res = models.task_info.objects.filter(pid_id=pid, endStatus=0, taskStatus=1)

                taskList = []
                if len(res) >1:
                    for t in res :
                        veh_res = models.vehicle_task.objects.filter(carNum_id = t.carNum_id)
                        taskListJson = param.taskListJson.format(t.current_task,
                                                                 t.carNum_id, t.taskType, t.taskStatus,
                                                                 veh_res[0].lon, veh_res[0].lat,
                                                                 veh_res[0].estimateTime, veh_res[0].odometry
                                                                 , [])
                        taskList.append(taskListJson)
                elif len(res ) == 1:
                    
                    pass
            pass
        if tasktype == 2 and taskstatus == 4:
            # if have_other_task():  changedTask()
            pass
    else:
        # need create app task 
        models.app_task.objects.create(pid_id = pid, lon = lon, lat = lat)

    # result = '{' + param.conformMsg.format( 0) + '}'
    return HttpResponse(result)
    # except :
    #     result = '{' + param.conformMsg.format(0, 2) + '}'
    #     return HttpResponse( result)
    pass

def reserve(request, pid, startlon, startlat, endlon, endlat):
    '''
    same area:  
    several area:
    inWhichArea(startlon, startlat)
    bDiffArea = False
    '''
    startArea = utils.inWhichArea(startlat, startlon)
    endArea = utils.inWhichArea(endlat, endlon)
    if startArea == 0 or endArea == 0 :
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    elif startArea == endArea:
        # insert into task_info
        try :
            models.task_info.objects.create(pid_id=pid, startlon = startlon, startlat = startlat,
                                            endlon = endlon, endlat = endlat, taskType = 1,
                                            taskStatus = 0)
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format( 1) + '}'
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
            result = '{' + param.conformMsg.format(0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format(1) + '}'
            return HttpResponse(result)
    pass

def run(request, pid):
    # try:
    res = models.task_info.objects.filter(pid_id = pid, current_task = True, endStatus=0)
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        if row.taskType == 1 and row.taskStatus == 4:
            models.task_info.objects.filter(pid_id=pid, current_task=True, endStatus=0).update(taskType=2, taskStatus=0)
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format( 1) + '}'
            return HttpResponse(result)
    pass

def park(request, pid, carNum):
    pass

def launch(request, pid, carNum):
    pass

def cancel(request, pid):
    print(pid )
    string  = "he {}".format( pid )
    return HttpResponse(string)
    pass

def register(request, pid, password):
    try:
        # print(pid, password)
        models.app_info.objects.create( pid = pid, pwd = password)
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(1 ) + '}'
        return HttpResponse( result)

    pass

def userLogin(request, pid, password):
    try:
        res = models.app_info.objects.filter( pid = pid, pwd = password, ptype = 1)
        if len(res) > 0:
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format(1) + '}'
            return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(2) + '}'
        return HttpResponse( result)
    pass

def adminLogin(request, pid, password):
    try:
        res = models.app_info.objects.filter( pid = pid, pwd = password, ptype=2)
        if len(res) > 0:
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format(1) + '}'
            return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(2) + '}'
        return HttpResponse( result)
    pass

def taskQuery(request, pid ):
    try:
        res = models.app_info.objects.filter( pid = pid)
        if len(res) > 0:
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format(1) + '}'
            return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(2) + '}'
        return HttpResponse( result)
    pass

def parkInfo(request, pid):
    pass

def unstartInfo(request, pid):
    pass

def vehicleInfo(request, pid, carNum):
    pass

def vehicleList(request, pid):
    pass

# current useless
def comformMsg(request, pid):
    pass