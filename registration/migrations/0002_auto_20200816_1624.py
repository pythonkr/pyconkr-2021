# Generated by Django 2.2.13 on 2020-08-16 07:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_patron', models.BooleanField(default=False)),
                ('ticket_purchase_datetime', models.DateTimeField(default=datetime.datetime(2020, 8, 16, 16, 24, 14, 265817))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='manualpayment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='option',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='user',
        ),
        migrations.DeleteModel(
            name='IssueTicket',
        ),
        migrations.DeleteModel(
            name='ManualPayment',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
    ]
