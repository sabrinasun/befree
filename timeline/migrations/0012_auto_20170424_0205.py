# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 07:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0011_auto_20170405_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategory',
            name='name_en',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='itemcategory',
            name='name_zh',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
