# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalaccount',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='externalaccount',
            unique_together=set([('name', 'shop')]),
        ),
    ]