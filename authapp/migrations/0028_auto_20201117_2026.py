# Generated by Django 3.1.2 on 2020-11-17 17:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0027_auto_20201115_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 19, 17, 26, 50, 81256, tzinfo=utc)),
        ),
    ]