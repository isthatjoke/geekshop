# Generated by Django 3.1.2 on 2020-10-28 12:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0017_auto_20201025_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 30, 12, 28, 14, 394643, tzinfo=utc)),
        ),
    ]
