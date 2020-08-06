from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.forms import PasswordInput
from django import forms

class CustomUser(AbstractUser):
    username = None
    re_password = forms.CharField(max_length=128, widget=PasswordInput(render_value=True))
    lastname = models.CharField(max_length=30,default='')
    firstname = models.CharField(max_length=30,default='')
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()
    # add additional fields in here




class LoginForm():
    re_password = forms.CharField(max_length=128, widget=PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 're_password']
        widgets = {
            'password': PasswordInput()
        }

class RegistrationForm(ModelForm):
    re_password = forms.CharField(max_length=128, widget=PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 're_password']
        widgets = {
            'password': PasswordInput()
        }
