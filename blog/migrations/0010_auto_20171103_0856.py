# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 03:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20171102_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 3, 26, 58, 566730, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 3, 26, 58, 565943, tzinfo=utc)),
        ),
    ]
