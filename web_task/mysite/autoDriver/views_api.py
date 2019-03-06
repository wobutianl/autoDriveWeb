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
            get 1,0, check car getTask, if get return 1,1 tasklist(without path) else return 0
            get 1,1, check car prepared , return 1,2 and taskList  else return 0                                                                                                                                                                            
            get 1,2, check car status , return 1, 3
            get 1,3, check car status ,
            get 1,4, return 0
            get 2,0, check car getTask, if get return 1,1 else return 0
            get 2,4, (one task : then change task status)
                     (two task : change two of the task )
        ''' 
        result = makeTaskList(pid, tasktype, taskstatus)
    else:
        # need create app task 
        models.app_task.objects.create(pid_id = pid, lon = lon, lat = lat)
        result = '{' + param.conformMsg.format( 0) + '}'

    return HttpResponse(result)
    # except :
    #     result = '{' + param.conformMsg.format(0, 2) + '}'
    #     return HttpResponse( result)
    pass

def makeTaskList( pid, taskType , taskStatus ):
    # make a task list from task_info table
    res = models.task_info.objects.filter(pid_id=pid, end_status=0)
    result = param.webToApp
    transferPoints = res[0].transfer_points
    taskList = []
    if len(res) == 1:

        veh_res = models.vehicle_task.objects.filter(car_num_id=res[0].car_num_id)
        taskListJson = param.taskListJson.format(res[0].current_task,
                                                 res[0].car_num_id, res[0].task_type, res[0].task_status,
                                                 veh_res[0].lon, veh_res[0].lat,
                                                 veh_res[0].estimate_time, veh_res[0].odometry
                                                 , res[0].path)
        taskList.append(taskListJson)
        pass
    elif len(res) == 2:
        # if 1, 0 : car get prepared then 1,1, path else return 0, 0
        if taskType in ( 1, 2)  and task_status == 0:
            res = models.task_info.objects.filter(pid_id=pid, end_status=0, task_status = 0)
            if len(res) > 0:
                for t in res:
                    veh_res = models.vehicle_task.objects.filter(car_num_id=t.car_num_id)
                    taskListJson = param.taskListJson.format(t.current_task,
                                                             t.car_num_id, 1, 0,
                                                             veh_res[0].lon, veh_res[0].lat,
                                                             veh_res[0].estimate_time, veh_res[0].odometry
                                                             , t.path)
                    taskList.append(taskListJson)
            else:
                for t in res:
                    veh_res = models.vehicle_task.objects.filter(car_num_id=t.car_num_id)
                    taskListJson = param.taskListJson.format(t.current_task,
                                                             t.car_num_id, t.task_type, t.task_status,
                                                             veh_res[0].lon, veh_res[0].lat,
                                                             veh_res[0].estimate_time, veh_res[0].odometry
                                                             , t.path)
                    taskList.append(taskListJson)
            pass
        else :
            for t in res:
                veh_res = models.vehicle_task.objects.filter(car_num_id=t.car_num_id)
                taskListJson = param.taskListJson.format(t.current_task,
                                                         t.car_num_id, t.task_type, t.task_status,
                                                         veh_res[0].lon, veh_res[0].lat,
                                                         veh_res[0].estimate_time, veh_res[0].odometry
                                                         , t.path )
                taskList.append(taskListJson)
    result = '{' +  result.format(transferPoints, taskList) + '}'
    return result

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
            models.task_info.objects.create(pid_id=pid, start_lon = startlon, start_lat = startlat,
                                            end_lon = endlon, end_lat = endlat, task_type = 1,
                                            task_status = 0)
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
            models.task_info.objects.create(pid_id=pid, start_lon = startlon, start_lat = startlat,
                                            end_lon = midLon, end_lat = midLat, task_type = 1,
                                            task_status = 0, transfer_points = transferPoints,
                                            current_task = True )
            models.task_info.objects.create(pid_id=pid, start_lon=midLon, start_lat=midLat,
                                            end_lon=endlon, end_lat=endlat, task_type=1,
                                            task_status=0, transfer_points=transferPoints,
                                            current_task=False )
            result = '{' + param.conformMsg.format(0) + '}'
            return HttpResponse(result)
        except:
            result = '{' + param.conformMsg.format(1) + '}'
            return HttpResponse(result)
    pass

def run(request, pid):
    # try:
    res = models.task_info.objects.filter(pid_id = pid, current_task = True, end_status=0)
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        if row.task_type == 1 and row.task_status == 4:
            models.task_info.objects.filter(pid_id=pid, current_task=True, end_status=0).update(
                task_type=2, task_status=0)
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
        # res = models.app_info.objects.filter( pid = pid)
        result = makeTaskList(pid, 0, 0)
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
