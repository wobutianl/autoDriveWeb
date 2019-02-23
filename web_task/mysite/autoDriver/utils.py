from shapely.geometry import Polygon, Point
from . import driveArea

def inWhichArea( lat, lon ):
    p = Point(lat, lon)
    if p.within(driveArea.areaA):
        return 1
    elif p.within(driveArea.areaB):
        return 2
    else:
        return 0
    pass

def chooseDock( startlat, startlon, areaNum):
    # just care about the distance from begin point to dock
    sp = Point(startlat, startlon)
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
