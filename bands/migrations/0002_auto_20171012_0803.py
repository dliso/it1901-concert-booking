# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='genre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bands.Genre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='band',
            name='sold_albums',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='band',
            name='total_streams',
            field=models.IntegerField(default=0),
        ),
    ]
