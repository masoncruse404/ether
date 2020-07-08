from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from .signals import object_viewed_signal
from .utils import get_client_ip
from core.signals import user_logged_in
from django.utils import timezone
from django.contrib.auth.signals import  user_logged_out 
from django.dispatch import receiver 
from profiles.models import Profile
User = settings.AUTH_USER_MODEL

FORCE_INACTIVE_USER_SESSION = getattr(settings, 'FORCE_INACTIVE_USER_SESSION',False)
FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE',False)
class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ipaddress = models.CharField(max_length=220, blank=True, null=True)
    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    objectid = models.PositiveIntegerField()
    contentobject = GenericForeignKey('contenttype','objectid')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed %s" %(self.contentobject,self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)

    new_view_obj = ObjectViewed.objects.create(
                user = request.user,
                ipaddress = get_client_ip(request),
                contenttype = c_type,
                objectid = instance.id
    )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ipaddress = models.CharField(max_length=220, blank=True, null=True)
    session_key = models.CharField(max_length=100,null=True,blank=True)    
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)
    starttime = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    endtime = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    duration = models.CharField(max_length=220, blank=True, null=True)
    userended = models.BooleanField(default=False)



    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended



def post_save_session_receiver(sender, instance, created, *args, **kwargs):
        if created:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
            for i in qs:
                i.end_session()
        if not instance.active and not instance.ended:
            instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=User)

def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
        if not created:
            if instance.is_active == False:
                qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
                for i in qs:
                    i.end_session()



    

def user_logged_in_receiver(sender, instance, request, *args, **kwrags):
        print(instance)
        session_key = request.session.session_key
        ipaddress = get_client_ip(request)
        user = instance
        prof = Profile.objects.get(user=user)
        print('logged in prof ',prof)
        prof.lastlogin = timezone.now()
        print(timezone.now())
        print('pro last ',prof.lastlogin)
        prof.save()
        UserSession.objects.create(
            user=user,
            ipaddress=ipaddress,
            session_key=session_key,
            starttime=timezone.now()
        )

if FORCE_INACTIVE_USER_SESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)

user_logged_in.connect(user_logged_in_receiver)



@receiver(user_logged_out) 
def _user_logged_out(sender, user, request, **kwargs):
    session_key = request.session.session_key
    ipaddress = get_client_ip(request)
    luser = user
    
    try:
        obj = UserSession.objects.get(
            user=luser,
            ipaddress=ipaddress,
            session_key=session_key
        )
        print('obj ',obj)
        obj.active = False
        obj.endtime = timezone.now()
        obj.userended = True
        obj.duration = obj.endtime - obj.starttime
        obj.save()
    except:
        print('admin')

