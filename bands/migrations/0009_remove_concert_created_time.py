# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 10:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0008_auto_20170928_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concert',
            name='created_time',
        ),
    ]