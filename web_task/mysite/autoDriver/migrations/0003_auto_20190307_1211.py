# Generated by Django 2.1.7 on 2019-03-07 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0002_vehicle_info_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_info',
            name='current_task',
            field=models.IntegerField(default=0),
        ),
    ]
