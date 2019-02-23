from django.db import models

# Create your models here.

class vehicle_info(models.Model):
    vid = models.AutoField(primary_key=True)
    available = models.BooleanField(default=True)
    vehicleType = models.FloatField(default=0.0)
    battery = models.FloatField(default=0.0)
    carNum = models.TextField()
    camera = models.BooleanField(default=True)
    lidar = models.BooleanField(default=True)
    radar = models.BooleanField(default=True)
    rtk = models.BooleanField(default=True)
    px2 = models.BooleanField(default=True)
    ipc = models.BooleanField(default=True)

    def __str__(self):
        vehicle_str = '''
        battery: %s
        carNum: %s
        camera: %s
        lidar: %s
        radar: %s
        rtk: %s
        ''',(self.battery, self.carNum, self.carNum, self.lidar, self.radar, self.rtk)
        return vehicle_str

class vehicle_task(models.Model):
    vid = models.ForeignKey( vehicle_info, on_delete=models.CASCADE )
    tid = models.IntegerField()
    pid = models.IntegerField()
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    taskType = models.IntegerField()
    taskStatus = models.IntegerField()
    velocity = models.FloatField(default=0.0)
    direction = models.FloatField(default=0.0)
    estimateTime = models.FloatField(default=0.0)
    odometry = models.FloatField(default=0.0)
    pass

class app_info(models.Model):
    pid = models.AutoField(primary_key=True)
    pwd = models.SlugField()

    pass

class app_task(models.Model):
    pid = models.ForeignKey(app_info, on_delete=models.CASCADE )
    taskType = models.IntegerField()
    taskStatus = models.IntegerField()
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)

    def __str__(self):
        return "taskType: " + self.taskType + "  taskStatus: " + self.taskStatus

    pass

class task_info(models.Model):
    vid = models.ForeignKey(vehicle_info, on_delete=models.CASCADE )
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

    def __str__(self):
        return self.tid + " " + self.startlon + " " + self.startlat + " " + self.endlon + " " + self.endlat
    pass