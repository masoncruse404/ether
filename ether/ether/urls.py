"""ether URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from core import views as core_views
from uploads import views as upload_views
from analytics import views as analytics_views
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash', analytics_views.dash, name='dash'),
    path('login/', core_views.login, name='login'),
    path('users/', include('core.urls'), name='users'),
    path('users/', include('django.contrib.auth.urls'), name='users'),
    path('', upload_views.mydrive, name='home'),
    path('uploads/', include('uploads.urls')),
    path('rootfolder/', upload_views.rootfolder, name='rootfolder'),
    path('sharedwithme/', upload_views.sharedwithme, name='sharedwithme'),
    path('uploadfileat/', upload_views.uploadfileat),
    path('trash/', upload_views.mydrivetrash, name='trash'),
    path('starred/', upload_views.allStarred, name='starred'),
    path('makesubfolder/', upload_views.makesubfolder, name='makesubfolder'),
    path('subfolder/<int:pk>/', upload_views.subfolder, name='subfolder'),
    url(r'^moveto/(?P<slug>[-\w]+)-(?P<pk>\d+)-(?P<fk>\d+)/$', upload_views.moveto, name='moveto'),
    url(r'^movefolderto/(?P<slug>[-\w]+)-(?P<pk>\d+)-(?P<fk>\d+)/$', upload_views.movefolderto, name='movefolderto'),
    url(r'^share/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.share, name='share'),
    url(r'^sharefolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.sharefolder, name='sharefolder'),
    url(r'^trash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.trash, name='trash'),
    url(r'^trashtable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.trashtable, name='trashtable'),
    url(r'^trashtablefolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.trashtablefolder, name='trashtablefolder'),
    url(r'^trashfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.trashfolder, name='trashfolder'),
    url(r'^download/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.download, name='download'),
    url(r'^downloadfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.downloadfolder, name='downloadfolder'),
    url(r'^star/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.star, name='star'),
    url(r'^rename/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.rename, name='rename'),
    url(r'^renametable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renametable, name='renametable'),
    url(r'^renamestar/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamestar, name='renamestar'),
    url(r'^renamestartable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamestartable, name='renamestartable'),
    url(r'^renametrash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renametrash, name='renametrash'),
    url(r'^renametrashtable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renametrashtable, name='renametrashtable'),
    url(r'^renamesub/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamesub, name='renamesub'),
    url(r'^renamefolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefolder, name='renamefolder'),
    url(r'^renamefoldertable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefoldertable, name='renamefoldertable'),
    url(r'^renamefoldertabletrash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefoldertabletrash, name='renamefoldertabletrash'),
    url(r'^renamefolderstar/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefolderstar, name='renamefolderstar'),
    url(r'^renamefolderstartable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefolderstartable, name='renamefolderstartable'),
    url(r'^renamesubfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamesubfolder, name='renamesubfolder'),
    url(r'^starfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.starfolder, name='starfolder'),
    url(r'^startablefolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.startablefolder, name='startablefolder'),
    url(r'^startable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.startable, name='startable'),
    url(r'^removestar/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removestar, name='removestar'),
    url(r'^removetrash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removetrash, name='removetrash'),
    url(r'^removetrashtable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removetrashtable, name='removetrashtable'),
    url(r'^renamefoldertrash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.renamefoldertrash, name='renamefoldertrash'),
    url(r'^removestartable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removestartable, name='removestartable'),
    url(r'^removetrashfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removetrashfolder, name='removetrashfolder'),
    url(r'^removetrashfoldertable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removetrashfoldertable, name='removetrashfoldertable'),
    url(r'^copyfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfolderview, name='copyfolder'),
    url(r'^copyfoldertable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfoldertableview, name='copyfoldertable'),
    url(r'^copyfile/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfile, name='copyfile'),
    url(r'^copyfiletrash/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfiletrash, name='copyfiletrash'),
    url(r'^copyfiletable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfiletable, name='copyfiletable'),
    url(r'^copyfiletrashtable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copyfiletrashtable, name='copyfiletrashtable'),
    url(r'^copystarfile/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copystarfile, name='copystarfile'),
    url(r'^copystarfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copystarfolderview, name='copystarfolder'),
    url(r'^copytrashfolder/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copytrashfolderview, name='copytrashfolder'),
    url(r'^copytrashfoldertable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copytrashfoldertableview, name='copytrashfoldertable'),
    url(r'^copystarfiletable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copystarfiletable, name='copystarfiletable'),
    url(r'^copystarfoldertable/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copystarfoldertableview, name='copystarfoldertable'),
    url(r'^copysubfile/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.copysubfile, name='copysubfile'),
    url(r'^file/(?P<slug>[-\w]+)-(?P<fid>\d+)/$',upload_views.file, name='file'),
    url(r'^removefolderstar/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', upload_views.removefolderstar, name='removefolderstar'),
    url(r'^ajax/validate_username/$', upload_views.validate_upload,                name='validate_upload'),
    url(r'^ajax/searchajax/$', upload_views.searchajax,                name='searchajax'),
    url(r'^ajax/shareajax/$', upload_views.shareajax,                name='shareajax'),


]



if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
