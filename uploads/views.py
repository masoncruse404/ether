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


BASE_DIR = settings.BASE_DIR
User = get_user_model()

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
    return render(request, 'uploads/my-drive-table.html', context)

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

    #get default non trash context
    context = getcontext(request)



    #add message and alert to context
    successmsg = f.name + ' removed from trash '
    context.update({'successmsg':successmsg})
    context.update({'successalert':1})

    return render(request, 'uploads/my-drive.html', context)

@login_required(login_url='/users/login/')
def removetrashfolder(request, slug, pk):
    #remove folder from trash
    f = Folder.objects.get(pk=pk)
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
def trash(request, slug, pk):
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
    folder_list = None
    image_list  = File.objects.all().filter(trash=True)
    image_list = File.objects.filter(owner=pro, trash=True) | File.objects.filter(trash=True, sharedwith=pro)
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g, trash=True)

    successmsg = ''
    size = 0
    f = File.objects.get(pk=pk)
    if(f.trash == True):
        if(os.path.exists(BASE_DIR+'/media/'+f.name)):
            if(os.path.getsize(BASE_DIR+'/media/'+f.name)):
                size = os.path.getsize(BASE_DIR+'/media/'+f.name)
            else:
                size = 0
            if(f.path):
                os.remove(HOMEDIR+'/ether/static'+str(f.path))
            pro.storage -= size
            pro.save()
            print("delete")
            print(f.path)

        f.delete()
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()

    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-trash.html', context)

@login_required(login_url='/users/login/')
def trashfolder(request, slug, pk):
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
    folder_list = None
    image_list  = File.objects.all().filter(trash=True)
    image_list = File.objects.filter(owner=pro, trash=True)
    f = Folder.objects.get(pk=pk)
    if(f.trash == True):
        if(os.path.exists(f.path)):
            shutil.rmtree(f.path)
        f.delete()
        print("delete")
        print(f.path)
        successmsg = f.name + ' has been deleted'
    else:
        successmsg = f.name + ' has been added to the trash'
        f.trash = True
        f.save()
    folder_list = Folder.objects.filter(owner=pro, trash=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-trash.html', context)

def allTrash(request):
    image_list  = File.objects.all().filter(trash=True)
    folder_list  = Folder.objects.all().filter(trash=True)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list:':folder_list}
    return render(request, 'home.html', context)

def allStarred(request):
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
    image_list = File.objects.filter(owner=pro,starred=True)
    all_folder_list = Folder.objects.filter(owner=pro,starred=True)
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g,starred=True)
    image_list  = File.objects.all().filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, "folder_list":folder_list, "storage":storage}
    return render(request, 'uploads/my-drive-star.html', context)

def star(request, slug, pk):
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
    f = File.objects.get(pk=pk)
    f.starred = True
    f.save()
    successmsg = f.name + ' is starred'
    image_list  = File.objects.all().filter(owner=pro,starred=True)
    folder_list = Folder.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list,'successalert':1,'successmsg':successmsg,'folder_list':folder_list}
    return render(request, 'uploads/my-drive-star.html', context)

def starfolder(request, slug, pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    all_folder_list = Folder.objects.filter(owner=pro)
    f = Folder.objects.get(pk=pk)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f.starred = True
    f.save()
    successmsg = f.name + ' is starred'
    image_list = File.objects.all().filter(starred=True,owner=pro)
    folder_list = Folder.objects.filter(owner=pro,starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list,'successalert':1,'folder_list':folder_list,'successmsg':successmsg}
    return render(request, 'uploads/my-drive-star.html', context)

def removestar(request, slug, pk):
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
    f = File.objects.get(pk=pk)
    f.starred = False
    f.save()
    warningmsg = f.name + ' has been removed from starred'
    image_list = File.objects.all().filter(starred=True,owner=pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list,"alert":1,"warningmsg":warningmsg}
    return render(request, 'uploads/my-drive-star.html', context)

def removefolderstar(request, slug, pk):
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
    f = Folder.objects.get(pk=pk)
    f.starred = False
    f.save()
    warningmsg = f.name + ' has been removed from starred'
    image_list = File.objects.all().filter(starred=True,owner=pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list,"alert":1,"warningmsg":warningmsg}
    return render(request, 'uploads/my-drive-star.html', context)


#rename file
@csrf_exempt
def rename(request, slug, pk):
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
    me = user.email
    image_list = File.objects.filter(owner=pro)


    image_list = File.objects.filter(owner=pro)
    print('rename view')
    f = File.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    os.chdir(BASE_DIR+'/media/')
    shutil.move(BASE_DIR+'/media/'+f.name, BASE_DIR+'/media/'+newname+'.'+f.file_type)

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

    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'me':me, 'storage':storage}

    return render(request, 'uploads/my-drive.html', context)

#rename a starred file
@csrf_exempt
def renamestar(request, slug, pk):
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
    me = user.email
    image_list = File.objects.filter(owner=pro, starred=True)
    folder_list = Folder.objects.filter(owner=pro,starred=True)


    print('rename view')
    f = File.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    os.chdir(BASE_DIR+'/media/')
    shutil.move(BASE_DIR+'/media/'+f.name, HOMEDIR+'/media/uploads/'+newname+'.'+f.file_type)

    f.name = 'uploads/' + newname +'.'+f.file_type
    print(f.path)
    f.file = f.name
    f.save()


    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'me':me, 'storage':storage}

    return render(request, 'uploads/my-drive-star.html', context)


#rename a file in a subfolder
@csrf_exempt
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

    print('rename view')
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
def renamefolder(request, slug, pk):

    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    me = user.email
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
                pass
            qa_list.append(image)


    image_list = File.objects.filter(owner=pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'me':me, 'storage':storage}
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    print(f.path)
    f.save()

    return render(request, 'uploads/my-drive.html', context)
#renames a starred root folder
@csrf_exempt
def renamefolderstar(request, slug, pk):

    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
    storagemb = getstoragemb(pro)
    storage = getstorage(pro)
    all_folder_list = Folder.objects.filter(owner=pro)
    me = user.email
    image_list = File.objects.filter(owner=pro,starred=True)
    folder_list = Folder.objects.filter(owner=pro, starred=True)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, 'folder_list':folder_list, 'me':me, 'storage':storage}
    f = Folder.objects.get(pk=pk)
    newname = request.POST.get('newname-q','')
    f.name = newname
    print(f.path)
    f.save()

    return render(request, 'uploads/my-drive-star.html', context)

#renames a child folder
@csrf_exempt
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
@csrf_exempt
def share(request, slug, pk):
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

    print("slug",slug)
    print("pk",pk)
    sharewith = request.POST.get('share-q','')
    print('sharewith',sharewith)
    exists = CustomUser.objects.filter(email=sharewith)
    sharepro = None
    if(exists):
        sharepro = Profile.objects.get(user=exists[0])
        f = File.objects.get(pk=pk)
        f.sharedwith.add(sharepro)
        print("sharedwith",f.sharedwith)
        f.save()
        print("fileshared")
        successmsg = 'shared with ' + sharewith
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list,  'storage':storage,'successalert':1,'successmsg':successmsg}
    else:
        warningmsg = sharewith + ' is not a user'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage,"alert":1,"warningmsg":warningmsg}



    return render(request, 'uploads/my-drive.html', context)


#need to find better solution
#in hindsight it might have been better to have profiles containing files instead of files containing profiles
#since # of profiles < # of files
#will correct in later version
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
    all_files = File.objects.all()
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    image_list = []
    for fi in all_files:
        print('fi',fi)
        print('fi shared',fi.sharedwith.all())
        sharedperson = fi.sharedwith.all()
        for person in sharedperson:
            print("person",person)
            if(person == pro):
                image_list.append(fi)
                print('image',fi)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"image_list":image_list, 'storage':storage, 'storagemb':storagemb}
    return render(request, 'uploads/my-drive.html', context)

#move file
@csrf_exempt
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
                    print('folder',fo)
                    fo.folderfiles.remove(obj)
                    print('no cap')
            print(obj)

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
def movefolderto(request, slug, pk, fk):
    #parent folder is the destination
    p = Folder.objects.get(pk=fk)

    #child folder is the source
    c = Folder.objects.get(pk=pk)

    #set childs parents to the destination
    c.parent = p
    p.children.add(c)

    #save

    c.save()
    p.save()

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
    folder_list = None
    if pro.gid != 0:
        g = Folder.objects.get(id=pro.gid)
        folder_list = Folder.objects.filter(parent=g)
    qa_list = []
    x = 0
    all_folder_list = Folder.objects.filter(owner=pro)

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                return render(request, 'uploads/my-drive.html', context)
            qa_list.append(image)
            context = {"email":email,"firstinitial":firstinitial,"name":name,"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}


    print("all folders")
    for fold in all_folder_list:
        print(fold)
    context = {"storagemb":storagemb,"image_list":image_list, "qa_list":qa_list, 'folder_list':folder_list, 'storage':storage, 'all_folder_list':all_folder_list}

    return render(request, 'uploads/subfolder.html', context)


#creates genesis folder if it is the first folder created
@csrf_exempt
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


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'error_404.html', data)


@csrf_exempt

#makes the created folder a child of the genesis folder
def rootfolder(request):
    foldername = request.POST.get('newfolder-q','')
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
        folder_list = Folder.objects.filter(parent=g)
    duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro)
    qa_list = []
    x = 0

    for image in image_list:
        if 'jpeg' or 'png' or 'jpg' in image.file_type:
            x = x + 1
            if x == 20:
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    if(duplicatenamecheck):
        warningmsg = foldername + ' already exists'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'qa_list':qa_list, 'alert':1, 'warningmsg':warningmsg, 'all_folder_list':all_folder_list}
        return render(request, 'uploads/my-drive.html', context)
    print(foldername)

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
    else:
        g = Folder.objects.get(id=pro.gid)
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
        folder_list = Folder.objects.filter(parent=g)
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
    foldername = request.POST.get('newsubfolder-q','')
    duplicatenamecheck = Folder.objects.filter(name=foldername, owner=pro)
    image_list = pf.folderfiles.all()
    folder_list = Folder.objects.filter(parent=pf)
    if(duplicatenamecheck):
        warningmsg = foldername + ' already exists'
        context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"warningmsg":warningmsg,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'alert':1, 'foldername':foldername, 'parent':pf}
        return render(request, 'uploads/subfolder.html', context)
    sf = Folder.objects.create(parent=pf, owner=pro, name=foldername, path=pf.path+'/'+foldername)
    os.chdir(pf.path)
    os.mkdir(foldername)
    pf.children.add(sf)
    pf.save()
    successmsg = 'uploads/subfolder ' + sf.name + ' created';
    folder_list = Folder.objects.filter(parent=pf)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage, 'foldername':foldername, 'parent':pf,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/subfolder.html', context)


def dupfilecheck(pro, fname, copynum):

    #check if filename exists for given user
    copycheck = File.objects.filter(owner=pro, name=fname)


    if(copycheck):
        #file name exists add copy number
        print('copynum',copynum)
        fname = fname.replace(str(copynum),'')
        fname = fname.replace('()','')
        split = fname.split(".")
        copynum += 1
        print('copynum',copynum)
        fname = split[0] + '(' + str(copynum) + ').' + split[1]
        return dupfilecheck(pro, fname, copynum)
    else:
        #file name is unique return true and filename
        print('dupnew ',fname)
        return 1, fname




@csrf_exempt
def copyfile(request,slug,pk):
    user = request.user
    pro = Profile.objects.get(user=user)
    email = user.email
    uid = request.session['userid']
    cuser = User.objects.get(id=uid)
    name = cuser.firstname + ' ' + cuser.lastname
    firstinitial = cuser.firstname[0]
    firstinitial = firstinitial.upper()
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
                break
            qa_list.append(image)
    all_folder_list = Folder.objects.filter(owner=pro)
    storage = getstorage(pro)
    storagemb = getstoragemb(pro)
    f = File.objects.get(pk=pk)
    fname = f.name.split(".")
    newfilename = fname[0] + 'copy.' + fname[1]
    copynum = 0
    x,y = dupfilecheck(pro,newfilename,copynum)
    print('fname ',y)
    print('newfilename ',newfilename)
    #check if a copy of the file
    if(dupfilecheck(pro,newfilename,copynum)):
        print('here')
        filecopy = File.objects.create(owner=f.owner,name=y,path=f.path,file=f.file,file_type=fname[1],size=f.size)
        filecopy.save()
        successmsg = 'created' + filecopy.name

    image_list = File.objects.filter(owner=pro)
    context = {"email":email,"firstinitial":firstinitial,"name":name,"storage":storage,"storagemb":storagemb,"all_folder_list":all_folder_list,"image_list":image_list, 'folder_list':folder_list, 'storage':storage,'successalert':1,'successmsg':successmsg}
    return render(request, 'uploads/my-drive.html', context)

@csrf_exempt
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
    x,y = dupfilecheck(pro,newfilename,copynum)
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

def validate_upload(request):
    file_field = request.POST.get('file_field', None)
    data = {
        'file_field':file_field
    }
    return JsonResponse(data)


def download(request, slug, pk):
    f = File.objects.get(id=pk)
    if(f.path):
        path = HOMEDIR+'/ether/static'
        path += f.path
        print('fromdownloaditem'+path)
        f0 = open(path, 'rb')
        myfile = DjangoFile(f0)
    else:
        myfile = f.file
    response = HttpResponse(myfile)
    response['Content-Disposition'] = 'attachment; filename=' + f.name
    return response

def makefolderzip(folder):
    files = folder.folderfiles.all()
    if(files):
        for fi in files:
            path = '/tmp/'+folder.name+'/'
            if not os.path.exists(path):
                os.makedirs(path)
            copy(BASE_DIR+'/media/'+fi.name,path+fi.name)

def makefolderchildren(folder):
    children = folder.children.all()
    for child in children:
        makefolderzip(child)
        if(child.children.all()):
            makefolderchildren(child)



def downloadfolder(request, slug, pk):
    f = Folder.objects.get(id=pk)
    print('fpath',f.path)
    #get all the files in the parent folder

    #get the parents children folders

    makefolderzip(f)
    children = f.children.all()
    if(children):
        for child in children:
            makefolderchildren(child)

    #copy files to folder
    #make zip






    print('fromdownloaditem'+f.path)
    print("folder name ",f.name)
    shutil.make_archive('/tmp/'+f.name, 'zip','/tmp/'+f.name)
    f0 = open('/tmp/'+f.name+'.zip', 'rb')
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
            name = File.file.name
            name = name.split('/')[1]
            print('fname ',name)
            if(os.path.getsize(BASE_DIR+'/media/'+user.email+'/'+name)):
                size = os.path.getsize(BASE_DIR+'/media/'+user.email+'/'+name)
            else:
                size = 0
            print('size is',size)
            ftype = File.file.name.split('.')[-1]
            print('the name ',name)
            File.name = name
            File.file_type = ftype;
            File.owner = pro
            File.size = size
            pro.storage += size
            pro.save()
            File.save()
            print(File)
            data = {'is_valid': True, 'name': File.file.name, 'url': File.file.url,'fileid':File.id}
        else:
            print('is_valid false')
            data = {'is_valid': False}
        return JsonResponse(data)

class ProgressBarUploadSubView(View):
    def get(self, request):
        photos_list = File.objects.all()
        return render(self.request, 'uploads/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        print('here');
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        user = request.user
        pro = Profile.objects.get(user=user)
        form.instance.owner = pro

        if form.is_valid():
            pk = request.session['fid']
            pf = Folder.objects.get(id=pk)
            print('money time ',pf.path)
            print('heee ',form)
            File = form.save()
            name = File.file.name
            name = name.split('/')[1]
            ftype = name.split('.',1)[1]
            print('fname ',name)
            if os.path.getsize(BASE_DIR+'/media/'+user.email+'/'+name):
                size = os.path.getsize(BASE_DIR+'/media/'+user.email+'/'+name)
            else:
                size = 0
            print('size is',size)
            ftype = File.file.name.split('.')[-1]
            File.name = name
            File.file_type = ftype
            File.owner = pro
            File.size = size
            File.save()
            pro.storage += size
            pro.save()
            pf = Folder.objects.get(id=pk)
            pf.folderfiles.add(File)
            print('pathhhh ',pf.path+'/'+File.name)
            print(File)
            data = {'is_valid': True, 'name': File.file.name, 'url': File.file.url, 'fileid':File.id}
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
