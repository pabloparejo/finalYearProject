#encoding:utf-8
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount
from .forms import LoginForm

from myWholeCloud.settings import SITE_URL

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
	 		"upload_path": SITE_URL + "api/upload/",
			"number_of_services": len(services),
	 		"services": services}

	obj = json.dumps(data)
	page_title = "Home"

	return render(request, 'index.html', locals())


@login_required()
def show_services(request):

	if request.COOKIES.has_key('service_added'):
		auth_finished = True
		if request.COOKIES.has_key('new_account'):
			new_account = request.COOKIES['new_account'] == 'True'
			uid = request.COOKIES['account_uid']
			try:
				service_added = request.COOKIES['service_added']
				if service_added == 'dropbox':
					client_email = DropboxAccount.objects.get(uid=uid).email
				else:
					client_email = DriveAccount.objects.get(uid=uid).email
			except:
				error = True
				auth_finished = False

	dropbox_accounts = DropboxAccount.objects.filter(user=request.user)
	drive_accounts = DriveAccount.objects.filter(user=request.user)

	dropbox = {	'accounts': dropbox_accounts,
				'class': 'dropbox',
				'name': 'Dropbox', 
				}
	drive = {	'accounts': drive_accounts,
				'class': 'google-drive',
				'name': 'Google Drive', 
				}
	services = [dropbox, drive]

	response = render(request, 'services.html', locals())

	response.delete_cookie('service_added', path="/")
	response.delete_cookie('new_account', path="/")
	response.delete_cookie('account_uid', path="/")

	return response

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
    title = "Login"
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, 'form.html', locals())


def user_logout(request):

	logout(request)

	return HttpResponseRedirect('/')