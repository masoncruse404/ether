# Generated by Django 3.0.7 on 2020-07-26 20:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_auto_20200726_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 20, 14, 41, 171726, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 20, 14, 41, 171709, tzinfo=utc)),
        ),
    ]
