# Generated by Django 2.1.7 on 2019-04-01 03:06

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0014_merge_20190311_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle_info',
            name='velocity',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='task_info',
            name='path',
            field=jsonfield.fields.JSONField(),
        ),
    ]
