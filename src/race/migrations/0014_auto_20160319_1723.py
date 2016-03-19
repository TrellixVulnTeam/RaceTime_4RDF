# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0013_racecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='avg_speed',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='finish_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='place',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]