from django.db import models

# Create your models here.

class vehicle_info(models.Model):
    vehicleType = models.FloatField(default=0.0)
    carNum = models.TextField(primary_key=True)
    # camera = models.BooleanField(default=True)
    # lidar = models.BooleanField(default=True)
    # radar = models.BooleanField(default=True)
    # rtk = models.BooleanField(default=True)
    # px2 = models.BooleanField(default=True)
    # ipc = models.BooleanField(default=True)

    def __str__(self):
        vehicle_str = ''
        return vehicle_str

class vehicle_task(models.Model):
    carNum = models.ForeignKey( vehicle_info, on_delete=models.CASCADE )
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    battery = models.FloatField(default=0.0)
    estimateTime = models.FloatField(default=0.0)
    odometry = models.FloatField(default=0.0)
    endTime = models.DateTimeField()
    haveTask = models.BooleanField(default=False)

    pass

class app_info(models.Model):
    # pid = models.AutoField(primary_key=True)
    pid = models.IntegerField(primary_key=True)
    pwd = models.SlugField()
    ptype = models.IntegerField(default=0)  # 0: user , 1: admin
    pass

class app_task(models.Model):
    pid = models.ForeignKey(app_info, on_delete=models.CASCADE )
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)

    def __str__(self):
        return 'pid' + self.pid 

    pass

class task_info(models.Model):
    carNum = models.ForeignKey(vehicle_info, on_delete=models.CASCADE )
    pid = models.ForeignKey(app_info, on_delete=models.CASCADE )
    tid = models.AutoField(primary_key=True)
    startlon = models.FloatField(default=0.0)
    startlat = models.FloatField(default=0.0)
    endlon = models.FloatField(default=0.0)
    endlat = models.FloatField(default=0.0)
    transferPoints = models.TextField(default='[]')
    path = models.TextField(default='[]')

    current_task = models.BooleanField(default=True)
    taskType = models.IntegerField(default=0)
    taskStatus = models.IntegerField(default=0)
    endStatus = models.IntegerField(default=0)
    # beSured = models.BooleanField(default=False)  # have vehicle get the task

    def __str__(self):
        return self.tid + " " + self.startlon + " " + self.startlat + " " + self.endlon + " " + self.endlat
    pass