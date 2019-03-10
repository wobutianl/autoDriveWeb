from django.shortcuts import render
from . import models
import json

from django.http import HttpResponse
from . import utils
from . import driveArea
from . import param
from . import views_web

'''
name format 
- for database : use **_**
- for param and get : use abbFee
'''

def index2(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#########################    APP  interface  ##############################################

# just update lon lat and make sure app get the msg
def update(request):
    #try:
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        lon = request.GET.get('lon', default='0.0')
        lat = request.GET.get('lat', default='0.0')
        taskType = request.GET.get('taskType', default='0')
        taskStatus = request.GET.get('taskStatus', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

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
        result = makeTaskList(pid, taskType, taskStatus)
    else:
        # need create app task 
        models.app_task.objects.create(pid_id = pid, lon = lon, lat = lat)
        result = '{' + param.conformMsg.format( 0) + '}'

    return HttpResponse(result)
    # except :
    #     result = '{' + param.conformMsg.format(0, 2) + '}'
    #     return HttpResponse( result)
    pass

def makeTaskList( pid, taskType, taskStatus ):
    # make a task list from task_info table
    res = models.task_info.objects.filter(pid=pid) # end_status=0
    result = param.webToApp
    transferPoints = res[0].transfer_points
    taskList = []
    if len(res) == 1:
        print( str(taskStatus)  +  "    " + str(res[0].task_status) )
        if int(taskStatus) == 1 and int(res[0].task_status) == 2 :
            print('have one task ' + res[0].car_num  + " get path ")
            veh_res = models.vehicle_info.objects.filter(car_num=res[0].car_num)
            taskjson = param.taskListJson
            taskjson[param.current_task_name] = res[0].current_task
            taskjson[param.vid_name] = res[0].car_num
            taskjson[param.task_type_name] = res[0].task_type
            taskjson[param.task_status_name] = res[0].task_status
            taskjson[param.lon_name] = veh_res[0].lon
            taskjson[param.lat_name] = veh_res[0].lat
            taskjson[param.estimate_name] = veh_res[0].estimate_time
            taskjson[param.odometry_name] = veh_res[0].odometry
            taskjson[param.path_name] = res[0].path

            taskList.append(taskjson)
        elif int(taskType) == 2 and int(taskStatus) == 4:
            print('have one task ' + res[0].car_num  + " end of the task ")
            models.task_info.objects.filter(tid = res[0].tid).delete()
            models.end_task_info.objects.create(pid=res[0].pid, tid=res[0].tid, 
                start_lon=res[0].start_lon, start_lat=res[0].start_lat, end_lon=res[0].end_lon, end_lat=res[0].end_lat, 
                transfer_points=res[0].transfer_points, path=res[0].path, car_num=res[0].car_num, end_status=1)
            taskList.append([])
        else:
            print('have one task ' + res[0].car_num )
            veh_res = models.vehicle_info.objects.filter(car_num=res[0].car_num)
            taskjson = param.taskListJson
            taskjson[param.current_task_name] = res[0].current_task
            taskjson[param.vid_name] = res[0].car_num
            taskjson[param.task_type_name] = res[0].task_type
            taskjson[param.task_status_name] = res[0].task_status
            taskjson[param.lon_name] = veh_res[0].lon
            taskjson[param.lat_name] = veh_res[0].lat
            taskjson[param.estimate_name] = veh_res[0].estimate_time
            taskjson[param.odometry_name] = veh_res[0].odometry
            taskjson[param.path_name] = [] # res[0].path

            taskList.append(taskjson)
            
        pass
    elif len(res) == 2:
        print('have two task ')
        cur_res = models.task_info.objects.filter(pid=pid, current_task = 1) #  end_status=0,
        # if 1, 0 : all the car get prepared then 1,1, path else return 0, 0
        if int(taskType) in ( 1, 2)  and int(taskStatus) == 0:
            res = models.task_info.objects.filter(pid=pid, task_status = 0) # end_status=0, 
            if len(res) > 0:
                for t in res:
                    veh_res = models.vehicle_info.objects.filter(car_num=t.car_num)
                    taskjson = param.taskListJson
                    taskjson[param.current_task_name] = t.current_task
                    taskjson[param.vid_name] = t.car_num
                    taskjson[param.task_type_name] = 1
                    taskjson[param.task_status_name] = 0 
                    taskjson[param.lon_name] = veh_res[0].lon
                    taskjson[param.lat_name] = veh_res[0].lat
                    taskjson[param.estimate_name] = veh_res[0].estimate_time
                    taskjson[param.odometry_name] = veh_res[0].odometry
                    taskjson[param.path_name] = [] # t.path
                    
                    taskList.append(taskjson)
            else:
                for t in res:
                    veh_res = models.vehicle_info.objects.filter(car_num=t.car_num)
                    taskjson = param.taskListJson
                    taskjson[param.current_task_name] = t.current_task
                    taskjson[param.vid_name] = t.car_num
                    taskjson[param.task_type_name] = t.task_type
                    taskjson[param.task_status_name] = t.task_status 
                    taskjson[param.lon_name] = veh_res[0].lon
                    taskjson[param.lat_name] = veh_res[0].lat
                    taskjson[param.estimate_name] = veh_res[0].estimate_time
                    taskjson[param.odometry_name] = veh_res[0].odometry
                    taskjson[param.path_name] = [] #t.path

                    taskList.append(taskjson)
            pass
        elif int(taskStatus) == 1 and int(cur_res[0].taskStatus) == 2 :
            for t in res:
                veh_res = models.vehicle_info.objects.filter(car_num=t.car_num)
                taskjson = param.taskListJson
                taskjson[param.current_task_name] = t.current_task
                taskjson[param.vid_name] = t.car_num
                taskjson[param.task_type_name] = t.task_type
                taskjson[param.task_status_name] = t.task_status 
                taskjson[param.lon_name] = veh_res[0].lon
                taskjson[param.lat_name] = veh_res[0].lat
                taskjson[param.estimate_name] = veh_res[0].estimate_time
                taskjson[param.odometry_name] = veh_res[0].odometry
                taskjson[param.path_name] = t.path

                taskList.append(taskjson)
        elif int(taskType) == 2 and int(taskStatus) == 4:
            # change current_task
            # models.task_info.objects.filter(pid=pid, end_status=0, current_task = 1).update(end_status = 1)
            models.task_info.objects.filter(pid=pid, current_task = 0).update(current_task = 1) # end_status=0, 
            res = models.task_info.objects.filter(pid=pid, current_task = 1) # end_status=0, 

            veh_res = models.vehicle_info.objects.filter(car_num=t.car_num)
            taskjson = param.taskListJson
            taskjson[param.current_task_name] = res[0].current_task
            taskjson[param.vid_name] = res[0].car_num
            taskjson[param.task_type_name] = res[0].task_type
            taskjson[param.task_status_name] = res[0].task_status 
            taskjson[param.lon_name] = veh_res[0].lon
            taskjson[param.lat_name] = veh_res[0].lat
            taskjson[param.estimate_name] = veh_res[0].estimate_time
            taskjson[param.odometry_name] = veh_res[0].odometry
            taskjson[param.path_name] = t.path

            taskList.append(taskjson)
        else:
            for t in res:
                veh_res = models.vehicle_info.objects.filter(car_num=t.car_num)
                taskjson = param.taskListJson
                taskjson[param.current_task_name] = t.current_task
                taskjson[param.vid_name] = t.car_num
                taskjson[param.task_type_name] = t.task_type
                taskjson[param.task_status_name] = t.task_status 
                taskjson[param.lon_name] = veh_res[0].lon
                taskjson[param.lat_name] = veh_res[0].lat
                taskjson[param.estimate_name] = veh_res[0].estimate_time
                taskjson[param.odometry_name] = veh_res[0].odometry
                taskjson[param.path_name] = [] #t.path

                taskList.append(taskjson)
    result = '{' +  result.format(0, transferPoints, taskList) + '}'
    return result

def reserve(request):
    '''
    '''
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        startLon = request.GET.get('startLon', default='0.0')
        startLat = request.GET.get('startLat', default='0.0')
        endLon = request.GET.get('endLon', default='0.0')
        endLat = request.GET.get('endLat', default='0.0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    startArea = utils.inWhichArea( float(startLat), float(startLon) )
    endArea = utils.inWhichArea( float(startLat), float(startLon) )
    if startArea == 0 or endArea == 0 :
        result = '{' + param.conformMsg.format(' not in the area ') + '}'
        return HttpResponse(result)
    elif startArea == endArea :
        # insert into task_info
        res = models.vehicle_info.objects.filter(available=1 , vehicle_type = startArea , battery__gt=50, have_task=0 ) # , battery__gt=50
        if len(res)>0:
        #try :
            print(pid)
            models.task_info.objects.create(pid=int(pid), start_lon = startLon, start_lat = startLat,
                                            end_lon = endLon, end_lat = endLat, task_type = 1,
                                            task_status = 0, current_task = 1, car_num = res[0].car_num)
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format( " s=e no suit car " + str(startArea) ) +  '}'
            return HttpResponse(result)
        #except:
        #    result = '{' + param.conformMsg.format( 1) + '}'
        #    return HttpResponse(result)
    else:
        dockNum = utils.chooseDock( float(startLat), float(startLon), startArea)
        transferPoints = [ driveArea.dockPoint[startArea-1][dockNum] ]
        midLat = driveArea.dockPoint[startArea-1][dockNum].x
        midLon = driveArea.dockPoint[startArea-1][dockNum].y
        
        #try :
        res_s = models.vehicle_info.objects.filter(available=True, vehicle_type = startArea, battery__gt=50 )
        res_e = models.vehicle_info.objects.filter(available=True, vehicle_type = endArea, battery__gt=50 )
        if len(res_s)>0 and len(res_e) >0:
            models.task_info.objects.create(pid=pid, start_lon = startLon, start_lat = startLat,
                                            end_lon = midLon, end_lat = midLat, task_type = 1,
                                            task_status = 0, transfer_points = transferPoints,
                                            current_task = 1, car_num = res[0].car_num )

            models.task_info.objects.create(pid=pid, start_lon=midLon, start_lat=midLat,
                                            end_lon=endLon, end_lat=endLat, task_type=1,
                                            task_status=0, transfer_points=transferPoints,
                                            current_task= 0, car_num = res[0].car_num )
            result = '{' + param.conformMsg.format(0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format( "s!=e have no car " ) + '}'
            return HttpResponse(result)
        # except:
        #     result = '{' + param.conformMsg.format(1) + '}'
        #     return HttpResponse(result)
    pass

def run(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    # try:
    res = models.task_info.objects.filter(pid = pid, current_task = True,) # end_status=0
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        if row.task_type == 1 and row.task_status == 4:
            models.task_info.objects.filter(pid=pid, current_task=True, ).update(
                task_type=2, task_status=0)  # end_status=0
            result = '{' + param.conformMsg.format( 0) + '}'
            return HttpResponse(result)
        else:
            result = '{' + param.conformMsg.format( 1) + '}'
            return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format(1 ) + '}'
    #    return HttpResponse( result)

def park(request ):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        carNum = request.GET.get('carNum',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    # try:
    res = models.task_info.objects.filter( pid = pid, ) #end_status=0 
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        models.task_info.objects.filter(pid=pid, ).update(
            task_type=3, task_status=0)  # end_status=0
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format(1 ) + '}'
    #    return HttpResponse( result)
    pass

def launch(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        carNum = request.GET.get('carNum',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    # try:
    res = models.task_info.objects.filter( pid = pid,  ) # end_status=0
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        models.task_info.objects.filter(pid=pid, ).update(
            task_type=5, task_status=0) # end_status=0
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format(1 ) + '}'
    #    return HttpResponse( result)
    pass

def cancel(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    # try:
    res = models.task_info.objects.filter( pid = pid,  ) # end_status=0
    if len(res) <= 0:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    for row in res:
        models.task_info.objects.filter(pid=pid, ).update(
            task_type=4, task_status=0) # end_status=0
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format(1 ) + '}'
    #    return HttpResponse( result)


def register(request):
    #try:
        # print(pid, password)
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        password = request.GET.get('password',default='110')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)


    models.app_info.objects.create( pid = pid, pwd = password, p_type=1)
    result = '{' + param.conformMsg.format( 0 ) + '}'
    return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format( 1 ) + '}'
    #    return HttpResponse( result)

    pass

def userLogin(request ):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        password = request.GET.get('password',default='110')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    #try:
    res = models.app_info.objects.filter( pid = pid, pwd = password, p_type = 1)
    if len(res) > 0:
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    #except :
    #    result = '{' + param.conformMsg.format(2) + '}'
    #    return HttpResponse( result)
    pass

def adminLogin(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        password = request.GET.get('password',default='110')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    try:
        res = models.app_info.objects.filter( pid = pid, pwd = password, p_type=2)
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

def taskQuery(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    try:
        # res = models.app_info.objects.filter( pid = pid)
        result = makeTaskList(pid, 0, 0)
    except :
        result = '{' + param.conformMsg.format(' no such user ') + '}'
    return HttpResponse( result)
    pass

def parkInfo(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    # 可泊车辆信息 
    pass

def unstartInfo(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    pass

def vehicleInfo(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
        carNum = request.GET.get('carNum',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    pass

def vehicleList(request):
    if request.method == 'GET':
        pid = request.GET.get('pid',default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    pass
