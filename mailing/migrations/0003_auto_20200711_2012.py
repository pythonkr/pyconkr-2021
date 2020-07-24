# Generated by Django 2.2.13 on 2020-07-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_mailing_sender_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='send_to_all_participant',
        ),
        migrations.AddField(
            model_name='mailing',
            name='send_to',
            field=models.CharField(choices=[('INFO', '정보성 메일'), ('AD', '광고성 메일'), ('NONE', '보내지 않음')], default='INFO', max_length=100),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='sender_name',
            field=models.CharField(default='PyCon Korea', max_length=100),
        ),
    ]
