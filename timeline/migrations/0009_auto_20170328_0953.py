# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0008_auto_20170315_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineitem',
            name='title_link',
            field=models.CharField(max_length=500),
        ),
    ]
