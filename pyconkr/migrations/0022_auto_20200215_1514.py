# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-15 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyconkr', '0021_tutorialproposal_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorialproposal',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
