# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 13:21
from __future__ import unicode_literals

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('users', 'User')

    for row in MyModel.objects.all():
        row.omics_uuid = uuid.uuid4()
        row.save(update_fields=['omics_uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_add_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
