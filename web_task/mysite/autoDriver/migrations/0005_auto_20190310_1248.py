# Generated by Django 2.1.7 on 2019-03-10 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0004_auto_20190308_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='end_task_info',
            fields=[
                ('car_num', models.TextField(max_length=128)),
                ('pid', models.IntegerField(default=0)),
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('start_lon', models.FloatField(default=0.0)),
                ('start_lat', models.FloatField(default=0.0)),
                ('end_lon', models.FloatField(default=0.0)),
                ('end_lat', models.FloatField(default=0.0)),
                ('transfer_points', models.TextField(default='[]')),
                ('path', models.TextField(default='[]')),
                ('end_status', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='task_info',
            name='end_status',
        ),
    ]
