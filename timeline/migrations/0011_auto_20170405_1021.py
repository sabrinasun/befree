# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0010_language_lang_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='lang_code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]