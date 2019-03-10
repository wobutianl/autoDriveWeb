from django.shortcuts import render
from . import models
import json


import time 
from datetime import datetime 
from django.views.decorators.csrf import csrf_exempt
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
        if haveTask == 1:
            models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat,available = available, battery=battery,
                estimate_time=estimateTime, odometry=odometry , have_task = 1)
        elif v_res[0].have_task == 1 and v_res[0].end_time != '0' :
            # res = models.task_info.objects.filter( car_num = carNum, end_status=0 )
            # if len(res)>0:
            #     if res[0].task_type == 2 and res[0].task_status == 4:
            cur_time = datetime.now()
            # print(cur_time)
            # print(utils.str2datetime(v_res[0].end_time) )
            # print( (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds )
            if  (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds > 120:
                models.vehicle_info.objects.filter(car_num=carNum).update(
                    lon=lon, lat=lat, available=available, battery=battery, 
                    estimate_time=0.0, odometry=0.0 ,have_task = 0, end_time='0' )
            else:
                models.vehicle_info.objects.filter( car_num=carNum ).update(
                    lon=lon, lat=lat, available=available, battery=battery, estimate_time=estimateTime, odometry=odometry )
        else: # when task belong to 1 0 , the first time to get task 
            res = models.task_info.objects.filter( car_num = carNum, task_type=1, task_status=0) # end_status=0, 
            if len(res)>0:
                result = {'taskType = 1 :  lon': res[0].start_lon, 'lat': res[0].start_lat}
                return HttpResponse( json.dumps(result) )
                
            res = models.task_info.objects.filter(car_num=carNum, task_type=1, task_status=1) # end_status=0, 
            if len(res) > 0:
                result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status}
                return HttpResponse( json.dumps(result) )

            res = models.task_info.objects.filter(car_num=carNum, task_type=2, task_status=0) # end_status=0, 
            if len(res) > 0:
                result = {'taskType = 2: lon': res[0].end_lon, 'lat': res[0].end_lat}
                return HttpResponse( json.dumps(result) )

            res = models.task_info.objects.filter(car_num=carNum, task_type=2, task_status=1) # end_status=0, 
            if len(res) > 0:
                result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status}
                return HttpResponse( json.dumps(result) )
            

            models.vehicle_info.objects.filter( car_num=carNum ).update(
                lon=lon, lat=lat, available=available, battery=battery , estimate_time=0.0, odometry=0.0)

    result = '{' + param.conformMsg.format( 0 ) + '}'
    return HttpResponse(result)
    pass


# error 
def makeVehicleTask(taskType, taskStatus):
    '''
    0 0 : have task then 1, 0 and end lon lat 
    1 0 : result 0 , 1 0 and task []
    1 2 : result 0 , 1 1 then begin () 
    1 3 :
    1 4 : get 1 4 then back to 1 0 
    '''
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
        models.task_info.objects.filter(car_num = carNum).update( task_status=1 )
        models.vehicle_info.objects.filter(car_num = carNum).update( have_task = 1 )
        result = '{' + param.conformMsg.format( 0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass

@csrf_exempt
def begin(request):
    print ('this is the request ', request.body )
    if (request.method == 'POST'):
        value = json.loads(request.body)
        if isinstance(value, dict):
            carNum = value['vid']
            vehicleType = value['vehicleType']
            path = value['path']
            estimateTime = value['estimateTime']
            odometry = value['odometry']
    else :
        if (request.method == 'GET'):
            result = '{' + param.conformMsg.format( ' request is GET ') + '}'
            return HttpResponse(result)
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # update task table
        models.task_info.objects.filter(car_num=carNum).update( task_status=2, path=path)
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
        models.task_info.objects.filter(car_num=carNum).update( task_status=3 )
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
        # just set end time when taskType = 2
        res = models.task_info.objects.filter(car_num=carNum, task_type=2 )
        if len(res)>0 :
            models.vehicle_info.objects.filter(car_num=carNum).update(end_time=str(datetime.now()) )
        result = '{' + param.conformMsg.format(0) + '}'
        return HttpResponse(result)
        pass
    else:
        result = '{' + param.conformMsg.format(1) + '}'
        return HttpResponse(result)
    pass