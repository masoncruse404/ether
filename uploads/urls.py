from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static

from . import views
app_name = 'uploads'
urlpatterns = [
        path('', views.mydrive),
        url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
        url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
        path('mydrive/', views.mydrive, name='mydrive'),
        path('mydrivetable/', views.mydrivetable, name='mydrivetable'),
        path('imagesearch/', views.mydrivetableimagesearch, name='mydrivetableimagesearch'),
        path('starred/', views.allStarred, name='allStarred'),
        path('recent/', views.recent, name='recent'),
        url(r'^ajax/validate_upload/$', views.validate_upload, name='validate_username'),
        url(r'^progress-bar-subupload/$', views.ProgressBarUploadSubView.as_view(), name='progress_bar_subupload'),
]

