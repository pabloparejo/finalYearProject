#encoding:utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect

import json
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount
from .forms import LoginForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# LOGIN REQUIRED UNTIL WE BUILD A WELCOME PAGE!!
@login_required()
def home(request):
	user = request.user
	dropbox_services = DropboxAccount.objects.filter(user=user)
	drive_services = DriveAccount.objects.filter(user=user)
	services = []
	for service in dropbox_services:
		services.append(service.get_path('/'))

	for service in drive_services:
		services.append(service.get_path('/'))

	data = {"bytes_total": "habria que ver esto",
	 		"bytes_used": "habria que ver esto",
			"number_of_services": len(services),
	 		"services": services}

	obj = json.dumps(data)
	page_title = "Home"

	return render(request, 'index.html', locals())
	return HttpResponseRedirect('/dropbox')


@login_required()
def show_services(request):

	page_title = 'New service'
	dropbox_accounts = DropboxAccount.objects.filter(user=request.user)
	drive_accounts = DriveAccount.objects.filter(user=request.user)

	dropbox = {	'accounts': dropbox_accounts,
				'id': 'dropbox',
				'name': 'Dropbox', 
				}
	drive = {	'accounts': drive_accounts,
				'id': 'google-drive',
				'name': 'drive', 
				}
	services = [dropbox, drive]

	return render(request, 'services.html', locals())

@login_required()
def delete_account(request, service, a_uid):
	if service == "dropbox":
		account = DropboxAccount.objects.get(uid=a_uid)
	else:
		account = DriveAccount.objects.get(uid=a_uid)

	account.delete()

	return HttpResponseRedirect('/services')

#---------- USERS ----------#

def new_user(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	titulo = "register"
	return render(request, 'form.html', locals())

def user_login(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, 'form.html', locals())


def user_logout(request):

	logout(request)

	return HttpResponseRedirect('/')