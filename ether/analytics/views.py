from django.shortcuts import render
from profiles.models import Profile
from django.utils import timezone
import json

from datetime import date, datetime, timedelta

# Create your views here.

#new users are users that have created an account
#within the last week
def getNewUsers(ndays):

	now = timezone.now()
	print('now ',now)
	weekago = now - timezone.timedelta(days=ndays)
	print('week ago ',weekago)
	profiles = Profile.objects.all()
	newuserlist = []
	for profile in profiles:
		if profile.creationdate >= weekago:
			#profile has been created within the last week
			newuserlist.append(profile)

	numofnewprofiles = len(newuserlist)
	print('numofnewprofiles ',numofnewprofiles)

	return numofnewprofiles

def getUserLabels():
	profiles = Profile.objects.all()
	labels = []
	for profile in profiles:
		if profile.lastlogin:
			labels.append(profile.user.email)

	return labels

def convertTime(time):
	print('convert time ', time)
	split = str(time).split(',')
	if len(split) > 1:
		split = str(split[0]).replace(" days","")
		split = int(split)

	else:
		split = str(split).split(":")[0].replace("['","")
		
		split = float(split)/24
		if not split:
			split = 1

		print('i am split ',split)
		

	print('days ',split)
	return split

def getTimeSinceLastLogin():
	profiles = Profile.objects.all()
	print('plen ',len(profiles))
	data = []
	for profile in profiles:
		if profile.lastlogin:
			print('here')
			time = timezone.now() - profile.lastlogin
			print('time ',time)
			if str(time).find(','):
				ftime = convertTime(time)
			print('time ',ftime)
			data.append(ftime)
			profile.timesincelastlogin = ftime
			profile.save()
		
	return data


def dash(request):
	numofdaysago = 7
	numofnewprofiles = getNewUsers(numofdaysago)
	data = getTimeSinceLastLogin()

	print('data size ',len(data))
	labels = getUserLabels()
	
	labels = labels[0:len(data)]

	return render(request, 'dashboard/index.html',{'numofnewusers':numofnewprofiles,'labels':labels,'size':len(data), 'timedata':data})
