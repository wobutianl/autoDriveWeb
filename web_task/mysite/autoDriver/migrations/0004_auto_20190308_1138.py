# Generated by Django 2.1.7 on 2019-03-08 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0003_auto_20190307_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_info',
            name='car_num',
            field=models.TextField(max_length=128, unique=True),
        ),
    ]