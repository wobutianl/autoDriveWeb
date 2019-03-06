from shapely.geometry import Polygon, Point
from . import driveArea


def inWhichArea( lat, lon ):
    p = Point(lat, lon)
    if p.within(driveArea.areaA):
        print(1)
        return 1
    elif p.within(driveArea.areaB):
        print(2)
        return 2
    else:
        return 0
    pass

def chooseDock( lat, lon, areaNum):
    # just care about the distance from begin point to dock
    sp = Point(lat, lon)
    if areaNum == 1:
        points = driveArea.dockPoint[0]
    elif areaNum == 2:
        points = driveArea.dockPoint[1]
    min_distance = 0.0
    dock_num = -1
    for p in points:
        i = 0
        d = sp.distance(p)
        if min_distance > d:
            dock_num = i
        i = i+1
    return dock_num


def getTaskStatus(app_taskType, app_taskStatus, v_taskType, v_taskStatus):
    taskType = 0
    taskStatus = 0
    if app_taskType > v_taskType:
        taskType = app_taskType
    elif app_taskType == v_taskType:
        if app_taskStatus >= v_taskStatus :
            taskStatus = app_taskStatus
        elif app_taskStatus < v_taskStatus:
            taskStatus = v_taskStatus
    return (taskType, taskStatus)
    pass
