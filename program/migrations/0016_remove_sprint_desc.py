# Generated by Django 2.2.13 on 2020-08-25 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0015_auto_20200825_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprint',
            name='desc',
        ),
    ]
