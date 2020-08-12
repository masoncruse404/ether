# Generated by Django 3.0.8 on 2020-07-07 17:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uploads.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0006_auto_20200707_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, max_length=500)),
                ('name', models.CharField(blank=True, max_length=75)),
                ('file_type', models.CharField(blank=True, max_length=75)),
                ('files', models.FileField(blank=True, upload_to=uploads.models.content_file_name)),
                ('size', models.CharField(blank=True, max_length=1000)),
                ('file', models.FileField(blank=True, default='', upload_to=uploads.models.user_directory_path)),
                ('images', models.ImageField(blank=True, upload_to='album')),
                ('starred', models.BooleanField(default=False)),
                ('trash', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(default=datetime.datetime(2020, 7, 7, 17, 10, 41, 739386, tzinfo=utc))),
                ('modified', models.DateTimeField(default=datetime.datetime(2020, 7, 7, 17, 10, 41, 739403, tzinfo=utc))),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_owner', to='profiles.Profile')),
                ('sharedwith', models.ManyToManyField(related_name='shared_with', to='profiles.Profile')),
                ('users', models.ManyToManyField(related_name='file_users', to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75)),
                ('path', models.CharField(blank=True, max_length=500)),
                ('starred', models.BooleanField(default=False)),
                ('trash', models.BooleanField(default=False)),
                ('gid', models.IntegerField(default=0)),
                ('children', models.ManyToManyField(related_name='_folder_children_+', to='uploads.Folder')),
                ('folderfiles', models.ManyToManyField(related_name='folderfiles', to='uploads.File')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_owner', to='profiles.Profile')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_parent', to='uploads.Folder')),
                ('users', models.ManyToManyField(related_name='folder_users', to='profiles.Profile')),
            ],
        ),
    ]
