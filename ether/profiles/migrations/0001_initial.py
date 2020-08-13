# Generated by Django 3.0.8 on 2020-07-07 17:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gid', models.IntegerField(default=0)),
                ('storage', models.IntegerField(blank=True, default=0)),
                ('capacity', models.IntegerField(default=15)),
                ('timesincelastlogin', models.CharField(blank=True, max_length=100, null=True)),
                ('creationdate', models.DateTimeField(default=datetime.datetime(2020, 7, 7, 17, 5, 31, 161310, tzinfo=utc))),
                ('lastlogin', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]