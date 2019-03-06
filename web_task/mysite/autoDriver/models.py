from django.db import models

# Create your models here.

class vehicle_info(models.Model):
    vehicle_type = models.FloatField(default=0.0)
    car_num = models.TextField(primary_key=True)
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
    car_num = models.ForeignKey( vehicle_info, on_delete=models.CASCADE )
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    battery = models.FloatField(default=0.0)
    estimate_time = models.FloatField(default=0.0)
    odometry = models.FloatField(default=0.0)
    # end_time = models.TextField()
    have_task = models.BooleanField(default=False)

    pass

class app_info(models.Model):
    pid = models.IntegerField(primary_key=True)
    pwd = models.TextField()
    p_type = models.IntegerField(default=0)  # 0: user , 1: admin
    pass

class app_task(models.Model):
    pid = models.ForeignKey(app_info, on_delete=models.CASCADE )
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)

    def __str__(self):
        return 'pid' + self.pid 

    pass

class task_info(models.Model):
    car_num = models.ForeignKey(vehicle_info, on_delete=models.CASCADE )
    pid = models.ForeignKey(app_info, on_delete=models.CASCADE )
    tid = models.AutoField(primary_key=True)
    start_lon = models.FloatField(default=0.0)
    start_lat = models.FloatField(default=0.0)
    end_lon = models.FloatField(default=0.0)
    end_lat = models.FloatField(default=0.0)
    transfer_points = models.TextField(default='[]')
    path = models.TextField(default='[]')

    current_task = models.BooleanField(default=True)
    task_type = models.IntegerField(default=0)
    task_status = models.IntegerField(default=0)
    end_status = models.IntegerField(default=0)
    # beSured = models.BooleanField(default=False)  # have vehicle get the task

    def __str__(self):
        return ''
    pass