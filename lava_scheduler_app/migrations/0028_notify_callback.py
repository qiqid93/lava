# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-19 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava_scheduler_app', '0027_device_dict_onto_filesystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='callback_content_type',
            field=models.IntegerField(blank=True, choices=[(0, 'urlencoded'), (1, 'json')], default=None, null=True, verbose_name='Callback content-type'),
        ),
        migrations.AddField(
            model_name='notification',
            name='callback_dataset',
            field=models.IntegerField(blank=True, choices=[(0, 'minimal'), (1, 'logs'), (2, 'results'), (3, 'all')], default=None, null=True, verbose_name='Callback dataset'),
        ),
        migrations.AddField(
            model_name='notification',
            name='callback_method',
            field=models.IntegerField(blank=True, choices=[(0, 'GET'), (1, 'POST')], default=None, null=True, verbose_name='Callback method'),
        ),
        migrations.AddField(
            model_name='notification',
            name='callback_token',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Callback token'),
        ),
        migrations.AddField(
            model_name='notification',
            name='callback_url',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Callback URL'),
        ),
    ]
