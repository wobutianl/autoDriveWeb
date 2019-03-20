conformMsg = ''' 'result':{} '''
webToVehicle = ''' 'tid':{}, 'lat':{}, 'lon':{} '''

webToApp = ''' 'result':{}, 'transferPoint':{}, 'taskList':{}, 'price':{}  '''
taskListJson = { 'currentTask':True, 'vid': '', 'taskType':0, 'taskStatus':0, 'vehicleLon':0, 'vehicleLat':0, 'estimateTime':0, 'odometry':0, 'path':[] }

RESERVER_TYPE = 1
GO_TYPE = 2

BEGIN_STATUS = 0 # app set the task
LAUNCH_STATUS = 1   # vehicle get the task
GO_STATUS = 2   # vehicle start run
END_STATUS = 3  # vehicle arrival

SQURE_CAR_TYPE = 1 # areaA , inside square
OUTSIDE_CAR_TYPE = 2 # areaB, outside square


current_task_name = 'currentTask'
vid_name = 'vid'
task_type_name = 'taskType'
task_status_name = 'taskStatus'
lon_name = 'vehicleLon'
lat_name = 'vehicleLat'
estimate_name = 'estimateTime'
odometry_name = 'odometry'
path_name = 'path'