# Generated by Django 2.1.7 on 2019-03-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0005_auto_20190310_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_task',
            name='have_task',
            field=models.IntegerField(default=0),
        ),
    ]
