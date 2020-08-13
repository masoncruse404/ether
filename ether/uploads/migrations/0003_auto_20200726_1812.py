# Generated by Django 3.0.7 on 2020-07-26 18:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20200726_1812'),
        ('uploads', '0002_auto_20200707_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='sharedwith',
            field=models.ManyToManyField(related_name='shared_with_folder', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 18, 12, 13, 9432, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 18, 12, 13, 9415, tzinfo=utc)),
        ),
    ]