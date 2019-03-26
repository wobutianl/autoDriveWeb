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