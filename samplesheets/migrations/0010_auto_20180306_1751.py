# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-06 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samplesheets', '0009_auto_20180228_1025'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='arc',
            index=models.Index(fields=['study', 'head_process'], name='samplesheet_study_i_b0ec92_idx'),
        ),
        migrations.AddIndex(
            model_name='arc',
            index=models.Index(fields=['study', 'head_material'], name='samplesheet_study_i_e38edd_idx'),
        ),
        migrations.AddIndex(
            model_name='arc',
            index=models.Index(fields=['assay', 'tail_process'], name='samplesheet_assay_i_de1733_idx'),
        ),
        migrations.AddIndex(
            model_name='arc',
            index=models.Index(fields=['assay', 'tail_material'], name='samplesheet_assay_i_bf0cd0_idx'),
        ),
        migrations.AddIndex(
            model_name='genericmaterial',
            index=models.Index(fields=['study', 'item_type'], name='samplesheet_study_i_408748_idx'),
        ),
    ]
