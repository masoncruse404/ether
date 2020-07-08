from django.contrib import admin
from .models import File
from .models import Folder

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
