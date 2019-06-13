# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-11 11:48
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samplesheets', '0006_update_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assay',
            name='characteristic_cat',
        ),
        migrations.RemoveField(
            model_name='assay',
            name='header',
        ),
        migrations.RemoveField(
            model_name='assay',
            name='unit_cat',
        ),
        migrations.RemoveField(
            model_name='process',
            name='scan_name',
        ),
        migrations.RemoveField(
            model_name='study',
            name='characteristic_cat',
        ),
        migrations.RemoveField(
            model_name='study',
            name='header',
        ),
        migrations.RemoveField(
            model_name='study',
            name='unit_cat',
        ),
        migrations.AddField(
            model_name='assay',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
        migrations.AddField(
            model_name='genericmaterial',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
        migrations.AddField(
            model_name='investigation',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
        migrations.AddField(
            model_name='investigation',
            name='parser_version',
            field=models.CharField(blank=True, help_text='Parser version', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='investigation',
            name='parser_warnings',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='Warnings from the previous parsing of the corresponding ISAtab'),
        ),
        migrations.AddField(
            model_name='process',
            name='first_dimension',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='First dimension (optional, for special case)'),
        ),
        migrations.AddField(
            model_name='process',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
        migrations.AddField(
            model_name='process',
            name='name_type',
            field=models.CharField(blank=True, help_text='Type of original name (e.g. Assay Name)', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='second_dimension',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='Second dimension (optional, for special case)'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
        migrations.AddField(
            model_name='study',
            name='headers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, help_text='Headers for ISAtab parsing/writing', size=None),
        ),
    ]
