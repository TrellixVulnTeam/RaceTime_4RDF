# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0009_auto_20160318_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='distance',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
