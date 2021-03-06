from django.db import models
import jsonfield

# Create your models here.

'''
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
'''

class vehicle_info(models.Model):
    vehicle_type = models.IntegerField(default=1) # 1:park, 2:public
    car_num = models.TextField(primary_key=True)
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    available = models.IntegerField(default=0)
    battery = models.FloatField(default=0.0)
    estimate_time = models.FloatField(default=0.0)
    odometry = models.FloatField(default=0.0)
    end_time = models.TextField(default='0')
    have_task = models.IntegerField(default=0)
    velocity = models.FloatField(default=0.0)

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
    have_task = models.IntegerField(default=0)

    task_type = models.IntegerField(default=0)
    task_status = models.IntegerField(default=0)
    

    def __str__(self):
        return 'pid' + self.pid 

    pass

class task_info(models.Model):
    car_num = models.TextField( max_length= 128, unique=True )
    pid = models.IntegerField(default=0 )
    tid = models.AutoField(primary_key=True)
    start_lon = models.FloatField(default=0.0)
    start_lat = models.FloatField(default=0.0)
    end_lon = models.FloatField(default=0.0)
    end_lat = models.FloatField(default=0.0)
    transfer_points = models.TextField(default='[]')
    path = jsonfield.JSONField()
    # path = models.TextField(default=[])
    price = models.FloatField(default=0.0)

    current_task = models.IntegerField(default=0)
    task_type = models.IntegerField(default=0)
    task_status = models.IntegerField(default=0)
    # end_status = models.IntegerField(default=0)
    app_park_enable_status = models.IntegerField(default=0)
    car_park_enable_status = models.IntegerField(default=0)

    def __str__(self):
        return ''
    pass

class end_task_info(models.Model):
    car_num = models.TextField( max_length= 128 )
    pid = models.IntegerField(default=0 )
    tid = models.AutoField(primary_key=True)
    start_lon = models.FloatField(default=0.0)
    start_lat = models.FloatField(default=0.0)
    end_lon = models.FloatField(default=0.0)
    end_lat = models.FloatField(default=0.0)
    transfer_points = models.TextField(default='[]')
    path = models.TextField(default='[]')
    price = models.FloatField(default=0.0)

    end_status = models.IntegerField(default=0)

    def __str__(self):
        return ''