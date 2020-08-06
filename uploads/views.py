from django.shortcuts import render
from django.db import transaction
from django import template
import os.path
from os import path as ospath
from django.db import transaction
from pathlib import Path
from django import template
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import Template
from django.http import HttpResponse
from django.http import JsonResponse
from .models import File, Folder, Photo
from profiles.models import Profile
from django.core.files import File as DjangoFile
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import time
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse

from django.contrib.auth import get_user_model

from .forms import PhotoForm
from .models import Photo
from core.models import CustomUser
from .forms import PhotoForm
from .models import Photo
from shutil import copy
from django.conf import settings
from analytics.signals import object_viewed_signal
import os
import pytz
import re
import shutil


lastParent = None

BASE_DIR = settings.BASE_DIR
User = get_user_model()

GENESIS = BASE_DIR + 'media/accounts'

def getgenesis(pro):
    genesis = BASE_DIR + '/media/accounts/' + str(pro.user.email) + '/genesis/'
    return genesis
def range(min=5):
    return range(min)



def getstoragemb(pro):
    storagemb = pro.storage
    storagemb = int(storagemb/1000000)
    print('storagemb is',storagemb)
    return storagemb

def getstoragegb(pro):
    storagemb = getstoragemb(pro)
    print('storagemb',storagemb)
    storagegb = storagemb/1024

    print('storagegb',storagegb)

    return storagegb

def getstorage(pro):
    storage = 100*getstoragegb(pro)
    storage = storage / pro.capacity
    print('storage is',storage)

    #format storage for progress bar
    storage = str(storage) + '%'

    return storage

#returns context for templates
def getcontext(request):
    user = request.user
    email = user.email
    print('email---',email)
    pro = Profile.objects.get(user=user)
    uid = request.session['userid']
    cuser = User.objects.get(email=email)
    print('cuser ',cuser)
    print('first name ',cuser.firstname)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    print('storage value ',storage)
    storagemb = getstoragemb(pro)

    print('storage value ',storage)
    me = user.email
    print('storagemb',storagemb)
    print('storage',storage)
    image_list = File.objects.filter(owner=pro,trash=False)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, trash=False)
    qa_list = []
    x = 0
    all_folder_list = Folder.objects.filter(owner=pro)

    if(image_list):
        for image in image_list:
            if 'jpeg' or 'png' or 'jpg' in image.file_type:
                x = x + 1
                if x == 20:
                    return con
                qa_list.append(image)
                con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}

    con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}
    return con

#get context for trash views

def getcontexttrash(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    me = user.email
    storage = getstorage(pro)
    print('storage value ',storage)
    storagemb = getstoragemb(pro)

    print('storage value ',storage)
    me = user.email
    print('storagemb',storagemb)
    print('storage',storage)
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, trash=True)
    all_folder_list = Folder.objects.filter(owner=pro)

    con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}
    return con


def getcontextstar(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    try:
        uid = request.session['userid']
        cuser = User.objects.get(id=uid)
        name = cuser.firstname + ' ' + cuser.lastname
        firstinitial = cuser.firstname[0]
        firstinitial = firstinitial.upper()
    except:
        name = ''
        firstinitial = ''
    
    me = user.email
    storage = getstorage(pro)
    print('storage value ',storage)
    storagemb = getstoragemb(pro)

    print('storage value ',storage)
    me = user.email
    print('storagemb',storagemb)
    print('storage',storage)
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    con = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, starred=True)
 
    all_folder_list = Folder.objects.filter(owner=pro)

    con = {"email":email,"firstinitial":firstinitial,"name":name,"me":me,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}
    return con



@login_required(login_url='/users/login/')
def recent(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = File.objects.filter(owner=pro)
    today_list = []
    week_list = []
    month_list = []
    year_list = []
    sep = ' '
    today = datetime.now()
    week = datetime.now() - timedelta(days=7)
    month = datetime.now() - timedelta(days=28)
    year = datetime.now() - timedelta(days=365)
    today = pytz.utc.localize(today)
    print("today", today)
    todaysplit = str(today).split()
    print("todaysplit", todaysplit[0])
    week = pytz.utc.localize(week)
    print("week", week)
    month = pytz.utc.localize(month)
    print("month", month)
    year = pytz.utc.localize(year)
    print("year", year)
    for image in image_list:
        rest = image.modified
        restsplit = str(rest).split()
        print("restsplit------",restsplit[0], todaysplit)
        #rest = pytz.utc.localize(rest)
        print(str(rest))
        if rest < year:
            year_list.append(image)
            print("year", image)
        elif rest <= month:
            month_list.append(image)
            print("month", image)
        elif rest <= week:
            week_list.append(image)
            print("week", image)
        elif str(restsplit[0]) ==  str(todaysplit[0]):
            today_list.append(image)
            print("today", image)


    context = {"email":email,"firstinitial":firstinitial,"name":name,"today_list":today_list, 'week_list':week_list, 'month_list':month_list, 'year_list':year_list, "storage":storage,"storagemb":storagemb}


    return render(request, 'uploads/recent.html', context)
@csrf_exempt
@login_required(login_url='/users/login/')
def mydrive(request):
    print('baseee ',settings.BASE_DIR)
    context = getcontext(request)
    print('context ',context)
    return render(request, 'uploads/my-drive.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetable(request):
    context = getcontext(request)
    return render(request, 'uploads/my-drive-table-old.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetableimagesearch(request):
    context = getcontext(request)
    return render(request, 'uploads/my-drive-table.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def mydrivetrash(request):

    context = getcontexttrash(request)

    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def removetrash(request, slug, pk):
    #remove file from trash
    f = File.objects.get(pk=pk)
    f.trash = False
    f.save()

    #get trash context
    context = getcontexttrash(request)



    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-trash.html', context)

@login_required(login_url='/users/login/')
def removetrashtable(request, slug, pk):
    #remove file from trash
    f = File.objects.get(pk=pk)
    f.trash = False
    f.save()

    #get trash context
    context = getcontexttrash(request)



    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def removetrashfolder(request, slug, pk):
    #remove folder from trash
    f = Folder.objects.get(pk=pk)
    for fi in f.folderfiles.all():
        fi.trash = False
        fi.save()
    f.trash = False
    f.save()


    #get default non trash context
    context = getcontext(request)


    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive.html', context)


@login_required(login_url='/users/login/')
def removetrashfoldertable(request, slug, pk):
    #remove folder from trash
    f = Folder.objects.get(pk=pk)
    for fi in f.folderfiles.all():
        fi.trash = False
        fi.save()
    f.trash = False
    f.save()


    #get default non trash context
    context = getcontext(request)


    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-old.html', context)


@login_required(login_url='/users/login/')
def trash(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)

    f = File.objects.get(pk=pk)
    if f.trash:
        if f.path:
            if os.path.isdir(f.path):  
                os.remove(f.path+'/'+f.name)
            elif os.path.isfile(path):  
                os.remove(f.path)
        pro.storage -= float(f.size)
        pro.save()
        f.delete()
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def trashtable(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    if f.trash:
        if f.path:
            os.remove(f.path)
           
            print("delete")
            print(f.path)
        pro.storage -= float(f.size)
        pro.save()
        f.delete()
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def trashfolder(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    if f.trash:
        dirwalkdelete(pro,f)
        successmsg = f.name + ' has been deleted'
        shutil.rmtree(f.path)
        f.delete()
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        dirwalktrash(pro,f)
        f.save()

    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    
    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def trashtablefolder(request, slug, pk):
    context = getcontexttrash(request)
    pro = Profile.objects.get(user=request.user)
    f = Folder.objects.get(pk=pk)
    if f.trash:
        if os.path.exists(f.path):
            shutil.rmtree(f.path)
        for fi in f.folderfiles.all():
            pro.storage -= fi.size
            pro.save()
            fi.delete()
        f.delete()
        print("delete")
        print(f.path)
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        dirwalktrash(pro,f)
        f.save()
    folder_list = Folder.objects.filter(owner=pro, trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-trash.html', context)



@login_required(login_url='/users/login/')
def allStarred(request):
    context = getcontextstar(request)
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def mydrivestartable(request):
    context = getcontextstar(request)
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def mydrivetrashtable(request):
    context = getcontexttrash(request)
    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def star(request, slug, pk):
    context = getcontextstar(request)

    f = File.objects.get(pk=pk)
    f.starred = True
    f.save()

    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-star.html', context)


@login_required(login_url='/users/login/')
def startable(request, slug, pk):
    pro = Profile.objects.get(user=request.user)
    #star file
    f = File.objects.get(pk=pk)
    f.starred = True
    f.save()
    successmsg = f.name + ' is starred'

    #get context
    context = getcontextstar(pro)
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def starfolder(request, slug, pk):

    f = Folder.objects.get(pk=pk)
    f.starred = True
    f.save()

    context = getcontextstar(request)
    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def startablefolder(request, slug, pk):
   
    f = Folder.objects.get(pk=pk) 
    f.starred = True
    f.save()
    
    context = getcontextstar(request)
    successmsg = f.name + ' is starred'
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def removestar(request, slug, pk):
    f = File.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})

  
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def removestartable(request, slug, pk):
   
    f = File.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def removefolderstar(request, slug, pk):
    
    f = Folder.objects.get(pk=pk)
    f.starred = False
    f.save()

    warningmsg = f.name + ' has been removed from starred'
    context = getcontextstar(request)
    context.update({'warningmsg':warningmsg})
    context.update({'alert':1})
    return render(request, 'uploads/my-drive-star.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def rename(request, slug, pk):
  
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,starred=isStarred)
    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontext(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    return render(request, 'uploads/my-drive.html', context)

#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,starred=isStarred)

    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontext(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    

    return render(request, 'uploads/my-drive-table-old.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametrashtable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,starred=isStarred,trash=True)
    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})
    return render(request, 'uploads/my-drive-table-trash.html', context)


#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renamestartable(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,starred=isStarred)
    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    context = getcontextstar(request)

    return render(request, 'uploads/my-drive-table-star.html', context)




#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renamestar(request, slug, pk):
    
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type
    if f.starred:
        isStarred = True
    else:
        isStarred = False
    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,starred=isStarred)
    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontextstar(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})

    return render(request, 'uploads/my-drive-star.html', context)

#rename file
@csrf_exempt
@login_required(login_url='/users/login/')
def renametrash(request, slug, pk):
  
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newname = request.POST.get('newname-q','')
    newname = newname+'.'+f.file_type

    filecopy = File.objects.create(owner=f.owner,name=newname,path=f.path,file=f.file,file_type=f.file_type,size=f.size,trash=True,starred=False)
    successmsg = 'renamed file ' + f.name + ' to file ' + filecopy.name
    f.delete()

    context = getcontexttrash(request)
    context.update({"successmsg":successmsg})
    context.update({"successalert":1})


    return render(request, 'uploads/my-drive-trash.html', context)


#rename a file in a subfolder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamesub(request, slug, pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    pf = Folder.objects.get(id=request.session['fid'])
    folder_list = Folder.objects.filter(parent=pf)
    image_list = pf.folderfiles.all()
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    me = user.email

    f = File.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    os.chdir(BASE_DIR+'/media/')
    shutil.move(BASE_DIR+'/media/'+f.name, HOMEDIR+'/media/'+newname+'.'+f.file_type)

    f.name = 'uploads/' + newname +'.'+f.file_type
    print(f.path)
    f.file = f.name
    f.save()

    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                pass

            qa_list.append(image)
    pf.folderfiles.add(f)
    pf.save()
    image_list = pf.folderfiles.all()
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'me':me, 'storage':storage, "parent":pf}

    return render(request, 'uploads/subfolder.html', context)

#displays one selected file
@login_required(login_url='/users/login/')
def file(request, slug,fid):
    print('fid ',fid)
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    f = File.objects.get(pk=fid)
    instance = f
    object_viewed_signal.send(instance.__class__,instance=instance,request=request)
    image_list = []
    image_list.append(f)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,'all_folder_list':all_folder_list, 'storage':storage,'instance':instance}
    return render(request, 'uploads/my-drive.html', context)


#renames a root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolder(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    f.save()

    context = getcontext(request)

    return render(request, 'uploads/my-drive.html', context)


#renames a root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertable(request, slug, pk):

    
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    f.save()

    context = getcontext(request)


    return render(request, 'uploads/my-drive-table-old.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertabletrash(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    f.save()

    context = getcontexttrash(request)
    return render(request, 'uploads/my-drive-table-trash.html', context)
#renames a starred root folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolderstar(request, slug, pk):

  
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    f.save()

    context = getcontextstar(request)

    return render(request, 'uploads/my-drive-star.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def renamefolderstartable(request, slug, pk):

    
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    f.save()

    getcontextstar(request)

    return render(request, 'uploads/my-drive-table-star.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def renamefoldertrash(request, slug, pk):

   
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
   
    f.save()

    return render(request, 'uploads/my-drive-trash.html', context)
#renames a child folder
@csrf_exempt
@login_required(login_url='/users/login/')
def renamesubfolder(request, slug, pk):

    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    print("session id ",request.session['fid'])
    pf = Folder.objects.get(id=request.session['fid'])
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    me = user.email

    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    print(f.path)
    f.save()
    folder_list = Folder.objects.filter(parent=pf)
    image_list = pf.folderfiles.all()
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"parent":f}

    return render(request, 'uploads/subfolder.html', context)


@login_required(login_url='/users/login/')
@csrf_exempt
def share(request, slug, pk):
    context = getcontext(request)
    sharewith = request.POST.get('share-q','')
    exists = CustomUser.objects.filter(email=sharewith)
    sharepro = None
    if(exists):
        sharepro = Profile.objects.get(user=exists[0])
        f = File.objects.get(pk=pk)
        sharepro.sharedfiles.add(f)
        sharepro.save()
        print("fileshared")
        successmsg = 'shared with ' + sharewith
        context.update({'successmsg':successmsg})
        context.update({'successalert':1})
    else:
        warningmsg = sharewith + ' is not a user'
        context.update({'warningmsg':warningmsg})
        context.update({'alert':1})

    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
@csrf_exempt
def sharefolder(request, slug, pk):
    context = getcontext(request)
    sharewith = request.POST.get('share-q','')
    exists = CustomUser.objects.filter(email=sharewith)
    sharepro = None
    if(exists):
        sharepro = Profile.objects.get(user=exists[0])
        f = Folder.objects.get(pk=pk)
        sharepro.sharedfolders.add(f)
        sharepro.save()
        context.update({'successmsg':successmsg})
        context.update({'successalert':1})
    else:
       warningmsg = sharewith + ' is not a user'
       context.update({'warningmsg':warningmsg})
       context.update({'alert':1})

    return render(request, 'uploads/my-drive.html', context)



@login_required(login_url='/users/login/')
def sharedwithme(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    print("pro",pro)
    all_files = pro.sharedfiles.all()
    all_folders = pro.sharedfolders.all()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = []
    folder_list = []
    for fi in all_files:
        image_list.append(fi)
        print('image',fi)
    for fi in all_folders:
        folder_list.append(fi)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"image_list":image_list, 'storage':storage, 'storagemb':storagemb,'folder_list':folder_list}
    return render(request, 'uploads/my-drive.html', context)

#move file
@csrf_exempt
@login_required(login_url='/users/login/')
def moveto(request, slug, pk, fk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)

    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    print('move to view')
    print('fk',fk)
    f = Folder.objects.get(pk=fk)
    fi = File.objects.get(pk=pk)
    fold = Folder.objects.all()
    for fo in fold:
        objs = fo.folderfiles.all()
        for obj in objs:
            if(obj == fi):
                if(obj.owner == fi.owner):
                    fo.folderfiles.remove(obj)

    #add file to folder
    fi.folder = f
    fi.save()
    f.folderfiles.add(fi)
    f.save()

    #how much memory the user has remaining
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)

    #check if file is moved to genesis folder
    if(pro.gid == f.id):
        print('genesis');
        image_list = File.objects.filter(owner=pro)
        folder_list = None
        if pro.gid != 0:
            g = Folder.objects.get(id=pro.gid)
            folder_list = Folder.objects.filter(parent=g)
        qa_list = []
        x = 0

        for image in image_list:
            if 'jpeg' or 'png' or 'jpg' in image.file_type:
                x = x + 1
                if x == 20:
                    return render(request, 'uploads/my-drive.html', context)
                qa_list.append(image)
                context = {"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage,'storagemb':storagemb}


        context = {"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage,'storagemb':storagemb, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive.html', context)

    #file is moved to subfolder
    else:
        f = Folder.objects.get(id=fk)
        folder_list = Folder.objects.filter(parent=f)
        image_list = f.folderfiles.all()
        all_folder_list = Folder.objects.filter(owner=pro)
        context = {"email":email,"firstinitial":firstinitial,"name":name,"all_folder_list":all_folder_list,"image_list":image_list,  'folder_list':folder_list, 'storage':storage,'storagemb':storagemb, 'all_folder_list':all_folder_list,"parent":f}
        return render(request, 'uploads/subfolder.html', context)

#move folder
@login_required(login_url='/users/login/')
def movefolderto(request, slug, pk, fk):
    user = request.user
    pro = Profile.objects.get(user=user)

    #parent folder is the destination
    p = Folder.objects.get(pk=fk)
    parentpath = p.path
    print('parentpath ',parentpath)

    #child folder is the source
    c = Folder.objects.get(pk=pk)
    childpath = c.path
    print('childpath ',childpath)
    
    #set childs parents to the destination
    c.parent = p
    p.children.add(c)


    #save

    c.save()
    p.save()
    
    genesis = getgenesis(pro)
    print('genesis ',genesis)

    print('child parent id ',c.parent.id)
    dirwalk(pro,c,p)
    print('c name=',c.name)
    
    shutil.move(childpath, parentpath) 

    context = getcontext(request)
    return render(request, 'uploads/my-drive.html', context)


#creates genesis folder if it is the first folder created
@csrf_exempt
@login_required(login_url='/users/login/')
def firstfolder(request):
    user = request.user
    pro = Profile.objects.get(user=user)

    path = BASE_DIR+'/media/'+ str(user)
    print(pro.gid)
    if pro.gid == 0:
        os.chdir(path)
        os.mkdir('genesis')
        path += '/genesis/'
        g = Folder.objects.create(path = path, owner=pro, name='genesis')

        os.chdir(path)
        f = Folder.objects.create(path = path+foldername, owner=pro, name=foldername, parent=g)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()

        pro.gid = g.id
        pro.save()

        return 1
    else:

        return 0



@csrf_exempt

#makes the created folder a child of the genesis folder
@login_required(login_url='/users/login/')
def rootfolder(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = File.objects.filter(owner=pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=False)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)


    foldername = request.POST.get('newfolder-q','')
    if foldername == '':
        warningmsg = 'enter a folder name'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive.html', context)
    path = BASE_DIR+'/media/accounts/'+ str(user)
    print(pro.gid)
    if pro.gid == 0:
        if os.path.exists(path):
            os.chdir(path)
        else:
            os.makedirs(path,exist_ok=True)
            os.chdir(path)
        path += '/genesis/'
        if not os.path.exists(path):
            os.mkdir('genesis')
        print('gpath = ',path)
        g = Folder.objects.create(path = path, owner=pro, name='genesis')

        duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=g)
        if(duplicatenamecheck):
            warningmsg = foldername + ' already exists'
            context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
            return render(request, 'uploads/my-drive.html', context)
        print(foldername)

     

        os.chdir(path)
        f = Folder.objects.create(path = path+foldername, owner=pro, name=foldername, parent=g)
        print('first folder path = ',path+foldername)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()

        pro.gid = g.id
        pro.save()
    else:
        g = Folder.objects.get(id=pro.gid)



        duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=g)
        if(duplicatenamecheck):
            warningmsg = foldername + ' already exists'
            context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
            return render(request, 'uploads/my-drive.html', context)
        print(foldername)
        print('g path  ' + g.path)
        f = Folder.objects.create(path = g.path+foldername, owner=pro, name=foldername, parent=g)
        os.chdir(g.path)
        os.mkdir(foldername)
        g.children.add(f)
        g.save()

        print('gid not 0')

    image_list = File.objects.filter(owner=pro)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=False)
    qa_list = []
    x = 0
    successmsg = foldername + ' created'
    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                return render(request, 'uploads/my-drive.html', context)
            qa_list.append(image)
            context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,'successalert':1,"successmsg":successmsg,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage}


    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"successmsg":successmsg,"all_folder_list":all_folder_list,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'successalert':1,'foldername':foldername}
    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
def subfolder(request, pk):
    request.session['fid'] = pk
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(id=pk)
    folder_list = Folder.objects.filter(parent=f)
    image_list = f.folderfiles.all()
    all_folder_list = Folder.objects.filter(owner=pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list,  'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list,"parent":f}
    return render(request, 'uploads/subfolder.html', context)


#makes the created folder a child of its direct parent
@csrf_exempt
@login_required(login_url='/users/login/')
def makesubfolder(request):
    pf = Folder.objects.get(id=request.session['fid'])
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = pf.folderfiles.all()
    folder_list = Folder.objects.filter(parent=pf)

    foldername = request.POST.get('newsubfolder-q','')
    if foldername == '':
        warningmsg = 'enter a folder name'
        context = {"alert":1,"warningmsg":warningmsg,"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'foldername':foldername, 'parent':pf}
        return render(request, 'uploads/subfolder.html', context)


    duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro, parent=pf)
   
    if(duplicatenamecheck):
        warningmsg = foldername + ' already exists'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"warningmsg":warningmsg,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'foldername':foldername, 'parent':pf}
        return render(request, 'uploads/subfolder.html', context)
    sf = Folder.objects.create(parent=pf, owner=pro, name=foldername, path=pf.path+'/'+foldername)
    os.chdir(pf.path)
    os.mkdir(foldername)
    pf.children.add(sf)
    pf.save()
    successmsg = 'subfolder ' + sf.name + ' created';
    folder_list = Folder.objects.filter(parent=pf)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'foldername':foldername, 'parent':pf,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/subfolder.html', context)

@login_required(login_url='/users/login/')
def dupfilecheck(pro, fname, copynum):

    #check if filename exists for given user
    copycheck = File.objects.filter(owner=pro, name=fname)

    oldname = None
    if(copycheck):
        #file name exists 
        #save original filename
        oldname = fname

        #add copy number
        print('copynum',copynum)
        fname = fname.replace(str(copynum),'')
        fname = fname.replace('()','')
        split = fname.split(".")
        copynum += 1
        print('copynum',copynum)
        if len(split) > 1:
            fname = split[0] + '(' + str(copynum) + ').' + split[1]
        else:
            fname = split[0] + '(' + str(copynum) + ')'
        return dupfilecheck(pro, fname, copynum)
    else:
        #file name is unique return true and filename
        print('dupnew file',fname)
        return 1, fname, oldname


@login_required(login_url='/users/login/')
def dupfoldercheck(pro, fname, copynum):

    #check if filename exists for given user
    copycheck = Folder.objects.filter(owner=pro, name=fname)


    if(copycheck):
        #file name exists add copy number
        print('copynum',copynum)
        fname = fname.replace(str(copynum),'')
        fname = fname.replace('()','')
        split = fname.split(".")
        copynum += 1
        print('copynum',copynum)
        fname = fname + '(' + str(copynum) + ')'
        return dupfoldercheck(pro, fname, copynum)
    else:
        #file name is unique return true and filename
        print('dupnew folder',fname)
        return 1, fname



@csrf_exempt
@login_required(login_url='/users/login/')
def copyfile(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletrash(request,slug,pk):
    pro = Profile.objects.get(user=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size,trash=True)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    context = getcontexttrash(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-trash.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletrashtable(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size,trash=True)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    image_list = File.objects.filter(owner=pro,trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-trash.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def copyfiletable(request,slug,pk):
    pro = Profile.objects.get(users=request.user)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-table-old.html', context)


@csrf_exempt
@login_required(login_url='/users/login/')
def copystarfile(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro,starred=True)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size,starred=True)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-star.html', context)

@csrf_exempt
@login_required(login_url='/users/login/')
def copystarfiletable(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro,starred=True)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    if len(fname) > 1:
        newfilename = fname[0] + 'copy.' + fname[1]
    else:
        newfilename = fname[0] + 'copy'
        fname.append('')

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size,starred=True)
        filecopy.save()
        pro.storage += float(filecopy.size)
        pro.save()
        successmsg = 'created copy ' + filecopy.name

    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-star.html', context)





@login_required(login_url='/users/login/')
def dirwalktrash(pro, pk):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    print('pf path ',pf.path)
    
    pf.trash = True

    if pf.folderfiles:
        
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            print('dirwlaktrash size ',f.size)
            f.trash = True
            f.save()
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalktrash(pro, child)
                
    return

@login_required(login_url='/users/login/')
def dirwalkdelete(pro, pk):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    print('pf path ',pf.path)
    
   

    if pf.folderfiles:
        
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            print('this is the deleted file size', f.size)
            pro.storage -= float(f.size)
            pro.save()
            f.delete()
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            dirwalkdelete(pro, child)
                
    return

@login_required(login_url='/users/login/')
def dirwalk(pro, pk, dst):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    print('dst path ',dst.path)
    children = pf.children.all()
    gen = getgenesis(pro)
    pf.path = dst.path + '/' + pf.path.replace(gen,'')
    print('pf path ',pf.path)
    pf.save()
    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            f.path = pf.path + '/' + f.name
            f.path = f.path.replace('/home/mason/projects/ether','')
            f.file.name = f.path
            f.save()
            print(f.path)
    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
        elif child.id == dst.id:
            #this is the dst
            pass
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            print('child path ', child.path)
            dirwalk(pro, child, dst)
    return


@login_required(login_url='/users/login/')
def dirwalkcopyfolder(pro, pk, argparent):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    x,copyname = dupfoldercheck(pro,pf.name,0)

    parentcopy = Folder.objects.create(owner=pf.owner,name=copyname,parent=argparent,path=argparent.path)
    print('split=',parentcopy.path.split('/',1))    
    parentcopy.path += parentcopy.name + '/'
    parentcopy.save()
    os.mkdir(parentcopy.path)
    print('parentcopy path=',parentcopy.path)

    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            x,copyname,tmp = dupfilecheck(pro,f.name,0)
 
            filecopy = File.objects.create(owner=f.owner,name=copyname,path=pf.path+'/'+f.name,file=f.file,size=f.size,file_type=f.file_type)
            filecopy.save()
            pro.storage += float(filecopy.size)
            pro.save()
            parentcopy.folderfiles.add(filecopy)
            pf.save()
            shutil.copyfile(pf.path+'/'+f.name,parentcopy.path+'/'+copyname)
            print('filecopy path=',filecopy.path)


    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
      
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            print('child path ', child.path)
            dirwalkcopyfolder(pro,child,parentcopy)
    return

@login_required(login_url='/users/login/')
def dirwalkstar(pro, pk, argparent):
    #pf = current folder
    pf = pk
    gid = pro.gid
    gf = Folder.objects.get(id=gid)
    children = pf.children.all()
    gen = getgenesis(pro)
    x,copyname = dupfoldercheck(pro,pf.name,0)

    parentcopy = Folder.objects.create(owner=pf.owner,name=copyname,parent=argparent,path=argparent.path,starred=True)
    print('split=',parentcopy.path.split('/',1))    
    parentcopy.path += parentcopy.name + '/'
    parentcopy.save()
    print('parentcopy path=',parentcopy.path)

    if pf.folderfiles:
        files = pf.folderfiles.all()
        #update the path of the files in the folder
        for f in files:
            x,copyname,tmp = dupfilecheck(pro,f.name,0)
 
            filecopy = File.objects.create(owner=f.owner,name=copyname,path=pf.path+'/'+f.name,file=f.file,size=f.size,file_type=f.file_type,starred=True)
            filecopy.save()
            pro.storage += float(filecopy.size)
            pro.save()
            parentcopy.folderfiles.add(filecopy)
            pf.save()
            print('filecopy path=',filecopy.path)


    for child in children:
        if child.id == pf.parent.id:
            #this is the parent id
            pass
      
        elif child.id == gf.id:
            #this is the genesis folder
            pass
        else:
            print('child path ', child.path)
            dirwalkstar(pro,child,parentcopy)
    return


@login_required(login_url='/users/login/')
def copyfolderview(request,slug,pk):
    f = Folder.objects.get(pk=pk)
    dirwalkcopyfolder(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
def copyfoldertableview(request,slug,pk):
    f = Folder.objects.get(pk=pk)
    dirwalkcopyfolder(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    context = getcontext(request)
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})
    return render(request, 'uploads/my-drive-table-old.html', context)

@login_required(login_url='/users/login/')
def copystarfolderview(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(pk=pk)
    dirwalkstar(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-star.html', context)

@login_required(login_url='/users/login/')
def copystarfoldertableview(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(pk=pk)
    dirwalkstar(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    image_list = File.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-star.html', context)

@login_required(login_url='/users/login/')
def copytrashfolderview(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(pk=pk)
    dirwalktrash(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    image_list = File.objects.filter(owner=pro,trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-trash.html', context)


@login_required(login_url='/users/login/')
def copytrashfoldertableview(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    image_list = File.objects.filter(owner=pro,trash=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,trash=True)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = Folder.objects.get(pk=pk)
    dirwalktrash(pro, f,f.parent)
    successmsg = 'copied folder ' + f.name
    image_list = File.objects.filter(owner=pro,trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-table-trash.html', context)

@login_required(login_url='/users/login/')
def copysubfile(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    pf = Folder.objects.get(id=request.session['fid'])
    folder_list = Folder.objects.filter(parent=pf)
    image_list = pf.folderfiles.all()
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newfilename = fname[0] + 'copy.' + fname[1]
    print('fname ',fname)
    print('newfilename ',newfilename)

    copynum = 0
    x,y, tmp = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size)
        filecopy.save()
        pf.folderfiles.add(filecopy)
        pf.save()
        successmsg = 'created' + filecopy.name

    image_list = pf.folderfiles.all()
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg,"parent":pf}

    return render(request, 'uploads/subfolder.html', context)



@csrf_exempt
@login_required(login_url='/users/login/')
def uploadfileat(request):
    firstfolder(request)
    pf = Folder.objects.get(id=request.session['fid'])
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        f = File.objects.create(owner=pro, name=myfile.name, folder=pf, path=pf.path+'/'+myfile.name)
        fs = FileSystemStorage(pf.path+'/')
        fs.save(myfile.name,myfile)
    folder_list = Folder.objects.filter(parent=pf)
    image_list = File.objects.filter(folder=pf)
    context = {'folder_list':folder_list}
    return render(request, 'uploads/subfolder.html', context)


@login_required(login_url='/users/login/')
def validate_upload(request):
    file_field = request.POST.get('file_field', None)
    data = {
        'file_field':file_field
    }
    return JsonResponse(data)

@login_required(login_url='/users/login/')
def download(request, slug, pk):
    f = File.objects.get(id=pk)
    user = request.user
    pro = Profile.objects.get(user=user)

    if(f.path):

        path = '/home/mason/projects/ether/'+f.file.name
        print('fromdownloaditem'+path)
        f0 = open(path, 'rb')
        myfile = DjangoFile(f0)
    else:
        myfile = f.file
    response = HttpResponse(myfile)
    response['Content-Disposition'] = 'attachment; filename=' + f.name
    return response




def downloadfolder(request, slug, pk):
    f = Folder.objects.get(id=pk)
   
    shutil.make_archive(f.path, 'zip',f.path)
    f0 = open('/'+f.path.strip("/")+'.zip', 'rb')
    myfile = DjangoFile(f0)

    #might remove files from folder after zip is created

    response = HttpResponse(myfile)
    response['Content-Disposition'] = 'attachment; filename=' + f.name+'.zip'
    return response


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = File.objects.all()
        return render(self.request, 'uploads/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        user = request.user
        pro = Profile.objects.get(user=user)
        form.instance.owner = pro

        if form.is_valid():
            File = form.save()
            url = File.file.name
            url = url[6:]
            print('p url ',url)
            name = File.file.name
            name = name.split('/')[-1]
            File.name = name
            path = File.file.path
            print('fname ',name)
            print('file url ',File.file.url)
            print('file path ',File.file.path)
            if os.path.getsize(path):
                size = os.path.getsize(path)
            else:
                size = 0            
            ftype = File.file.name.split('.')[-1]
            print('the name ',name)
            print('this is the path: ',File.file.path)
            File.file_type = ftype;
            File.owner = pro
            fpath = File.file.path
            fpath = fpath.replace('/home/mason/projects/ether/','')
            File.file.name = '/' + fpath
            print('fname ',File.file.name)
            File.size = size
            File.save()
            pro.storage += size
            pro.save()
            print(File)
            data = {'is_valid': True, 'name': File.name, 'url': File.file.name,'fileid':File.id}
        else:
            print('is_valid false')
            data = {'is_valid': False}
        return JsonResponse(data)

class ProgressBarUploadSubView(View):
    def get(self, request):
        photos_list = File.objects.all()
        return render(self.request, 'uploads/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        user = request.user
        pro = Profile.objects.get(user=user)
        form.instance.owner = pro

        if form.is_valid():

            if 'fid' in request.session:
                pk = request.session['fid']
                pf = Folder.objects.get(id=pk)
                form.instance.path = pf.path
            File = form.save()
            name = File.file.name
            name = name.split('/')[-1]
            File.name = name
            print('parent folder path ',pf.path)
            fpath = File.file.path
            oldpath = fpath
            fpath = fpath.replace(BASE_DIR,'')
            File.file.name = fpath
            print('filename ',File.file.name)
            print('money time ',pf.path)
            print('heee ',form)
            print('name= ',name)
        
            pf = Folder.objects.get(id=pk)
            pf.folderfiles.add(File)
            print('pathhhh ',pf.path+'/'+name)
            path = pf.path+'/'+name
            path = path.replace(BASE_DIR,'')
            ftype = File.file.name.split('.')[-1]
            File.file_type = ftype
            File.owner = pro

            
            print('oldpath', oldpath)
            if os.path.getsize(oldpath):
                size = os.path.getsize(oldpath)
                print('this is the size ',size)
            else:
                size = 0  
            #File.path =  pf.path+File.name
            File.size = size
            File.save()
            print('the file size is now ',File.size)

            pro.storage += size
            pro.save()
       
            data = {'is_valid': True, 'name': File.name, 'url': File.file.name,'fileid':File.id, 'fsize':size}
        else:
            print('is_valid false')
            data = {'is_valid': False}
        return JsonResponse(data)

class ProgressBarUploadSubViewOld(View):
    def get(self, request):
        photos_list = File.objects.all()
        return render(self.request, 'uploads/my-drive.html', {'photos': photos_list})

    def post(self, request):
        print('here');
        form = PhotoForm(self.request.POST, self.request.FILES)
        user = request.user
        pro = Profile.objects.get(user=user)
        form.instance.owner = pro
        if 'fid' in request.session:
            pk = request.session['fid']
            pf = Folder.objects.get(id=pk)
            pathname = pf.path
        else:
            pk = None
            pf = None
            pathname = ''
        form.instance.path = pathname
        if form.is_valid():
            File = form.save()
            name = File.file.name
            name = name.split('/')[-1]
            File.name = name
            print('parent folder path ',pf.path)
            fpath = File.file.path
            fpath = fpath.replace(BASE_DIR,'')
            File.file.name = '/' + fpath
            print('filename ',File.file.name)
            print('money time ',pf.path)
            print('heee ',form)
            print('name= ',name)
        
            pf = Folder.objects.get(id=pk)
            pf.folderfiles.add(File)
            print('pathhhh ',pf.path+'/'+name)
            path = pf.path+'/'+name
            path = path.replace(BASE_DIR,'')
            ftype = File.file.name.split('.')[-1]
            File.file_type = ftype
            File.owner = pro

            print('new subfile path = ',path)
            oldpath = path
            File.file.name = path
            if os.path.getsize(path):
                size = os.path.getsize(path)
            else:
                size = 0  
            File.size = size
            #File.path =  pf.path+File.name
            File.save()
            pro.storage += size
            pro.save()
            
            print(File)
            data = {'is_valid': True, 'name': File.name, 'url': oldpath, 'fileid':File.id}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            photo.owner
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

@csrf_exempt
def shareajax(request):
    print('in shareajax')
    user = request.user
    pro = Profile.objects.get(user=user)
    f = None
    if request.is_ajax and request.method == "POST":
        shareq = request.POST['shareq']
        print(shareq)


        if(User.objects.filter(email__contains=shareq).exists()):
            f = User.objects.filter(email__contains=shareq)


    return render(None,'ajaxshare.html', {'files':f})

@csrf_exempt
def searchajax(request):
    user = request.user
    pro = Profile.objects.get(user=user)
    searchq = request.GET.get('searchq', None)
    if request.method == "POST":
        searchq = request.POST['searchq']
    print('in search')
    print(searchq)
    f_json = False
    if(File.objects.filter(name__contains=searchq).exists()):
            f = File.objects.filter(name__contains=searchq, owner=pro)

    data = {
        'is_taken': f_json
    }
    return render(None,'uploads/ajax_search.html', {'files':f})
