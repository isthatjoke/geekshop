# Generated by Django 3.1.2 on 2020-12-01 19:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0029_auto_20201117_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 19, 44, 0, 482733, tzinfo=utc)),
        ),
    ]
