# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_remove_uuid_null'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecteventobjectref',
            name='object_pk',
        ),
        migrations.AddField(
            model_name='projecteventobjectref',
            name='object_uuid',
            field=models.UUIDField(blank=True, help_text='Object Omics UUID', null=True),
        ),
    ]