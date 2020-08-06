from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
from django.utils import timezone
import os

MAX_STORAGE = 15000000
HOMEDIR = os.environ['HOME']

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gid = models.IntegerField(default=0)
    storage = models.IntegerField(default=0, blank=True)
    capacity = models.IntegerField(default=15)
    timesincelastlogin = models.CharField(max_length=100, blank=True,null=True)
    creationdate = models.DateTimeField(default=timezone.now())
    lastlogin = models.DateTimeField(blank=True,null=True)
    sharedfiles = models.ManyToManyField("uploads.File", related_name='sharedfiles')
    sharedfolders = models.ManyToManyField("uploads.Folder", related_name='sharedfolders')

    def __str__(self):
        return self.user.email




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pro = Profile.objects.create(user=instance)
        path = '/home/mason/projects/ether/static/accounts/'
        os.chdir(path)
        os.mkdir(path + instance.email)
        pro.save()


        print("CREATED")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

