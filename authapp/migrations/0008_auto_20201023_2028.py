# Generated by Django 3.1.2 on 2020-10-23 20:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20201023_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 20, 28, 5, 395424, tzinfo=utc)),
        ),
    ]