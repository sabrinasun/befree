# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_auto_20170304_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineitem',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timeline.Teacher'),
        ),
    ]
