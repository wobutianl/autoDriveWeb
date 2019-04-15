from django.shortcuts import render

from django.http import HttpResponse
from . import models
import json 
from django.core import serializers
from django.http import JsonResponse

def index(request):
    vehicle_list = models.vehicle_info.objects.filter(lon__gt=0, lat__gt=0) # .values('car_num','lon','lat')
    json_data = serializers.serialize("json", vehicle_list)

    task_list = models.task_info.objects.filter(tid__gt = 0)
    json_task_data = serializers.serialize("json", task_list)

    # vehicle_list 
    return render(request,"index.html", {'vehicle_list': json_data, 'vehicle_info': vehicle_list, 'task_info': json_task_data})

def ajax_dict(request, car_num):
    # result = ''' 'vehicle':{} , 'task':{} '''
    vehicle_list = models.vehicle_info.objects.filter(car_num = car_num, lon__gt=0, lat__gt=0) # .values('car_num','lon','lat')
    json_vehicle_data = serializers.serialize("json", vehicle_list)
    
    task_list = models.task_info.objects.filter(car_num = car_num)
    json_task_data = serializers.serialize("json", task_list)

    return JsonResponse({"vehicle": json_vehicle_data, "task": json_task_data}, safe=False )
    
def cancel_task(request, carnum):
    models.task_info.objects.filter(car_num=carnum).delete()
    models.vehicle_info.objects.filter(car_num=carnum).update(have_task=0)
    
    return HttpResponse("canceled")
    
def show_info(request, carnum):
    result = r''' "vehicle_num":{} , "battery":{}, "longitude": {}, "latitude": {}, "velocity": {}, "path":{}, "status":{} '''
    task_list = models.task_info.objects.filter(car_num = carnum)
    path = "[]"
    status = "0"
    lon = "0.0"
    lat = "0.0"
    vel = "0.0"
    bat = "0.0"
    
    if len(task_list)>0:
        path=str(task_list[0].path).replace("'", "\"")
        status = int(task_list[0].task_status)
        str_status = ""
        if status == 0:
            str_status = "no task"
        elif status == 1:
            str_status = "have order"
        elif status in(2,3 ):
            str_status = "running"
        elif status == 4:
            str_status = "arrival"
        # result.format(status = str_status)
    vehicle_list = models.vehicle_info.objects.filter(car_num =carnum) 
    if len(vehicle_list)>0:
        bat=vehicle_list[0].battery
        lon=vehicle_list[0].lon
        lat=vehicle_list[0].lat
        vel=0.0 # vehicle_list[0].lat
        
    result = result.format(carnum, bat, lon, lat, vel, path , status )

    return JsonResponse( '{' + result +'}' , safe=False )

    
def nullmax_vehicle_info(request ):
    result = r''' "vehicle_num":"nullmax007" , "battery":{}, "longitude": {}, "latitude": {}, "velocity": {}, "path":{}, "status":{} '''
    # .values('car_num','lon','lat')

    path = "[]"
    status = "0"
    lon = "0.0"
    lat = "0.0"
    vel = "0.0"

    bat = "0.0"

    task_list = models.task_info.objects.filter(car_num = "nullmax007")
    if len(task_list)>0:
        path=str(task_list[0].path).replace("'", "\"")
        status = int(task_list[0].task_status)
        str_status = ""
        if status == 0:
            str_status = "no task"
        elif status == 1:
            str_status = "have order"
        elif status in(2,3 ):
            str_status = "running"
        elif status == 4:
            str_status = "arrival"
        # result.format(status = str_status)
    vehicle_list = models.vehicle_info.objects.filter(car_num = "nullmax007") 
    if len(vehicle_list)>0:
        bat=vehicle_list[0].battery
        lon=vehicle_list[0].lon
        lat=vehicle_list[0].lat
        vel=0.0 # vehicle_list[0].lat
        
    result = result.format(bat, lon, lat, vel, path , status )


    return JsonResponse( '{' + result +'}' , safe=False )
