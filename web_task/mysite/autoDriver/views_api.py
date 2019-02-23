from django.shortcuts import render

from django.http import HttpResponse

def index2(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def updateApp(request, pid, lon, lat, tasktype, taskstatus):
    print(pid, lon, lat, tasktype, taskstatus)

    pass

def setStartTask(request, pid, startlon, startlat, endlon, endlat):
    print(pid, startlat)
    pass

def setParkTask(request, pid, vid):
    pass

def setLaunchTask(request, pid, vid):
    pass

def setCancelTask(request, pid):
    print(pid )
    return HttpResponse("Hello, world. ", pid)
    pass

def setRegisterTask(request, pid, password):
    pass

def setLoginTask(request, pid, password):
    pass

def getParkInfo(request, pid):
    pass

def getUnStartInfo(request, pid):
    pass

def getVehicleInfo(request, pid, vid):
    pass

def getVehicleIdInfo(request, pid):
    pass

def haveGetMsg(request, pid):
    pass