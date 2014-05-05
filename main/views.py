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

# Create your views here.

def home(request):
	# drive = DriveAccount()
	# dropbox1 = DropboxAccount()
	# dropbox2 = DropboxAccount()

	# services = [drive.get_path('/'), dropbox1.get_path('/'), dropbox2.get_path('/')]

	# data = {"username": "request.user",
	# 		"number_of_services": len(services),
	# 		"total_size": "habria que ver esto",
	# 		"used_size": "habria que ver esto",
	# 		"services": services}

	# obj = json.dumps(data)
	page_title = "home"

	return render(request, 'index.html', locals())
	return HttpResponseRedirect('/dropbox')


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