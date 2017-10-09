# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0004_concert_genre_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='band_name',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bands.Band'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='concert',
            name='genre_music',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bands.Genre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='concert',
            name='stage_name',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bands.Stage'),
            preserve_default=False,
        ),
    ]