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
@csrf_exempt
def update(request):
    if request.method == 'GET':
        carNum = request.GET.get('carNum',default='0')
        vehicleType = request.GET.get('vehicleType', default=0)
        available = request.GET.get('available', default=1)
        lon = request.GET.get('lon', default=0)
        lat = request.GET.get('lat', default=0)

        haveTask = request.GET.get('haveTask', default=0)
        battery = request.GET.get('battery',default=0)
        estimateTime = request.GET.get('estimateTime', default=0)
        odometry = request.GET.get('odometry', default=1)
        velocity = request.GET.get('velocity', default = '0.0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    taskType = 0
    taskStatus = 0
    v_res = models.vehicle_info.objects.filter( car_num = carNum, vehicle_type=vehicleType)
    # print("the lens of vehicle ", len(v_res), carNum, vehicleType)
    if len(v_res) == 0: # register in db
        models.vehicle_info.objects.create(car_num=carNum, vehicle_type = vehicleType,lon=lon, lat=lat,available = available, battery=battery,
                    estimate_time=estimateTime, odometry=odometry , velocity = velocity, have_task = 0, end_time = '0' )
    else:   # have msg in task table or not
        t_res = models.task_info.objects.filter( car_num = carNum )
        if len(t_res)>0:
            taskType = t_res[0].task_type
            taskStatus = t_res[0].task_status
            #print("taskType:", taskType)
            #print("taskStatus:", taskStatus)
            # print("the car have task ")
            models.vehicle_info.objects.filter( car_num=carNum ).update(
                        lon=lon, lat=lat,available = available, battery=battery, velocity = velocity,
                    estimate_time=estimateTime, odometry=odometry , have_task = 1)
                # res = models.task_info.objects.filter( car_num = carNum )
            # when task belong to 1 0 , the first time to get task 

            res = models.task_info.objects.filter( car_num = carNum, task_type=1, task_status=0 ) # end_status=0, 
            if len(res)>0:
                result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status , 'lon': res[0].start_lon, 'lat': res[0].start_lat }
                #print ("start_lon", res[0].start_lon)
                #print("start_lat", res[0].start_lat)
                return HttpResponse( json.dumps(result) )

            #res = models.task_info.objects.filter(car_num=carNum, task_type=1 ) # end_status=0, , task_status = 0
            #if len(res) > 0:
            #    result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status}
            #    # print('get task', result)
            #    return HttpResponse( json.dumps(result) )

            res = models.task_info.objects.filter(car_num=carNum, task_type=2, task_status = 0 ) # end_status=0, 
            if len(res) > 0:
                result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status, 'lon': res[0].end_lon, 'lat': res[0].end_lat}
                # print("end_lon", res[0].end_lon)
                return HttpResponse( json.dumps(result) )

            res = models.task_info.objects.filter(car_num=carNum, task_type=2, task_status=1) # end_status=0, 
            if len(res) > 0:
                result = {'taskType': res[0].task_type, 'taskStatus': res[0].task_status}
                #print('run, ',result)
                return HttpResponse( json.dumps(result) )
            
            #res = models.task_info.objects.filter(car_num=carNum, task_status=4) # end_status=0, 
            #if len(res) > 0:
            #    models.task_info.objects.filter(car_num=carNum).delete()
            #    result = {'taskType': 0, 'taskStatus':0}
            #    return HttpResponse(json.dumps(result))

            res = models.task_info.objects.filter(car_num=carNum, task_type=4 )
            if len(res)>0:
                models.task_info.objects.filter(car_num=carNum).delete()
                result = {'taskType': 0, 'taskStatus':0}
                return HttpResponse(json.dumps(result))
                    
            result = {'taskType': taskType, 'taskStatus': taskStatus }
            #print("resp update taskType:", taskType)
            #print("resp update taskStatus:", taskStatus)
            #print('no special', result)
            return HttpResponse( json.dumps(result) )
            
        else : # have no task 
             models.vehicle_info.objects.filter( car_num=carNum ).update(
                        lon=lon, lat=lat,available = available, battery=battery, velocity = velocity,
                    estimate_time=estimateTime, odometry=odometry , have_task = 0)
 
         # vehicle arrivaled beyonged 2mintes
        if int(v_res[0].have_task) == 1 and v_res[0].end_time != '0' :
            # res = models.task_info.objects.filter( car_num = carNum, end_status=0 )
            # if len(res)>0:
            #     if res[0].task_type == 2 and res[0].task_status == 4:
            cur_time = datetime.now()
            # print(cur_time)
            # print(utils.str2datetime(v_res[0].end_time) )
            # print( (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds )
            if  (cur_time - utils.str2datetime(v_res[0].end_time) ).seconds > 120:
                models.vehicle_info.objects.filter(car_num=carNum).update(
                    lon=lon, lat=lat, available=available, battery=battery, velocity = velocity,
                    estimate_time=0.0, odometry=0.0 ,have_task = 0, end_time='0' )
               
    #print("resp update taskType:", taskType)
    #print("resp update taskStatus:", taskStatus)
    result = {'taskType': taskType, 'taskStatus': taskStatus }
    # print(result)
    return HttpResponse( json.dumps(result) )
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
@csrf_exempt
def getTask(request):
    if request.method == 'GET':
        carNum = request.GET.get('carNum',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    taskType = 0
    taskStatus = 0
    if len(v_res) > 0:
        res = models.task_info.objects.filter(car_num = carNum, task_type__in=[4]) # 
        if len(res) > 0 :
            models.task_info.objects.filter(car_num = carNum).delete()
            result = '{' + param.conformMsg.format( 0 ) + '}'
            return HttpResponse(result)
            
        res = models.task_info.objects.filter(car_num = carNum, task_type__in=[1,2,3], task_status=0)
        if len(res) > 0 :
            taskType = res[0].task_type
            taskStatus = res[0].task_status
            #print("get task taskType:", taskType)
            #print("get task taskStatus:", taskStatus)
            models.task_info.objects.filter(car_num = carNum).update( task_status=1 )
            models.vehicle_info.objects.filter(car_num = carNum).update( have_task = 1 )
            result = '{' + param.conformMsg.format( 10 ) + '}'
            return HttpResponse(result)
        

    # result = '{' + param.conformMsg.format(1) + '}'
    #print("resp get taskType:", taskType)
    #print("resp get taskStatus:", taskStatus)
    result = {'taskType': taskType, 'taskStatus': taskStatus }
    return HttpResponse(json.dumps(result))
    pass

@csrf_exempt
def begin(request):
    #print ('this is the request ', request.body )
    if (request.method == 'POST'):
        value = json.loads(request.body)
        if isinstance(value, dict):
            carNum = value['carNum']
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
        res = models.task_info.objects.filter(car_num = carNum, task_type__in=[1,2,3], task_status=1)
        if len(res) > 0 :
            models.task_info.objects.filter(car_num=carNum).update( task_status=2, path = path  ) 
            result = '{' + param.conformMsg.format(11) + '}'
            return HttpResponse(result)

    result = '{' + param.conformMsg.format(1) + '}'
    return HttpResponse(result)
    
@csrf_exempt
def cancel(request):
    if request.method == 'GET':
        carNum = request.GET.get('carNum',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)
    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        #print("have the car")
        res = models.task_info.objects.filter(car_num = carNum)
        if len(res) > 0 :
          # update task table
          models.task_info.objects.filter(car_num=carNum).delete()
          result = '{' + param.conformMsg.format(0) + '}'
          return HttpResponse(result)

    result = '{' + param.conformMsg.format(1) + '}'
    return HttpResponse(result)

@csrf_exempt
def run(request):
    if request.method == 'GET':
        carNum = request.GET.get('carNum',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')

    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        #print("have the car")
        res = models.task_info.objects.filter(car_num = carNum, task_type__in=[1,2,3] )
        if len(res) > 0 :
          # update task table
          models.task_info.objects.filter(car_num=carNum).update( task_status=3 )
          result = '{' + param.conformMsg.format(12) + '}'
          return HttpResponse(result)

    result = '{' + param.conformMsg.format(1) + '}'
    return HttpResponse(result)
    pass

@csrf_exempt
def arrival(request):
    if request.method == 'GET':
        carNum = request.GET.get('carNum',default='0')
        vehicleType = request.GET.get('vehicleType', default='0')
    else :
        result = '{' + param.conformMsg.format( ' request error ') + '}'
        return HttpResponse(result)

    v_res = models.vehicle_info.objects.filter(car_num=carNum, vehicle_type=vehicleType)
    if len(v_res) > 0:
        # just set end time when taskType = 2
        res = models.task_info.objects.filter(car_num=carNum, task_type__in=[1,2,3],task_status = 3 )
        if len(res)>0 :
            models.task_info.objects.filter(car_num=carNum).update( task_status=4 )
            res = models.task_info.objects.filter(car_num=carNum, task_type=2, task_status = 3 )
            if len(res)>0:
                models.vehicle_info.objects.filter(car_num=carNum).update(end_time=str(datetime.now()) )
            result = '{' + param.conformMsg.format(13) + '}'
            return HttpResponse(result)

    result = '{' + param.conformMsg.format(1) + '}'
    return HttpResponse(result)
    pass
