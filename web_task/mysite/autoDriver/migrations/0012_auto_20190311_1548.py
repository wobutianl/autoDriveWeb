# Generated by Django 2.1.7 on 2019-03-11 07:48

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autoDriver', '0011_auto_20190311_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_info',
            name='path',
            field=jsonfield.fields.JSONField(),
        ),
    ]