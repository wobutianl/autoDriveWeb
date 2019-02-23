from django.shortcuts import render
from . import models

from django.http import HttpResponse
from . import utils
from . import driveArea
import param

def index2(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def updateApp(request, pid, lon, lat, tasktype, taskstatus):
    try:
        res = models.app_task.objects.filter( pid_id = pid )
        # for row in res:
        #     return HttpResponse(row.pid)
        if len(res) > 0:
            models.app_task.objects.filter(pid_id =pid).update(taskType = tasktype, taskStatus = taskstatus,
                                                           lon = lon, lat = lat )
        else:
            models.app_task.objects.create(pid_id = pid, taskType = tasktype, taskStatus = taskstatus,
                                                           lon = lon, lat = lat)
        result = '{' + param.conformMsg.format(0, 0) + '}'
        return HttpResponse(result)
    except :
        result = '{' + param.conformMsg.format(0, 2) + '}'
        return HttpResponse( result)
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
                                            current_task = True)
            models.task_info.objects.create(pid_id=pid, startlon=midLon, startlat=midLat,
                                            endlon=endlon, endlat=endlat, taskType=1,
                                            taskStatus=0, transferPoints=transferPoints,
                                            current_task=False)
            result = '{' + param.conformMsg.format(0, 0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format(0, 1) + '}'
            return HttpResponse(result)
        return
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