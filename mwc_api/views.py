#encoding:utf-8
from django.shortcuts import render
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount, CredentialsModel

from django.http import HttpResponseNotFound

from apiclient.http import MediaInMemoryUpload
from apiclient.discovery import build

from dropbox.client import DropboxClient
from oauth2client.django_orm import CredentialsField

from itertools import chain

from django.http import HttpResponse

import json, httplib2

# Create your views here.

def display_api(request):
	data = {'description': 'Here we display our api',
			'urls': []}
	return HttpResponse(json.dumps(data), content_type="application/json")

def get_user_home(request):
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
	 		"username": user.username,
	 		"services": services}

	return data

def get_path(request, service=None, a_uid=None, path=None):

	if service == None:
		data = get_user_home(request)
	else:
		if path == "": #Path is passed by view get_path
			path = "/"

		if service == "dropbox":
			account = DropboxAccount.objects.get(uid=a_uid)
		elif service == "google-drive":
			account = DriveAccount.objects.get(uid=a_uid)

		data = account.get_path(path)

	return HttpResponse(json.dumps(data), content_type="application/json")

def delete_account(request, service, a_uid):
	try:
		if service == "dropbox":
			account = DropboxAccount.objects.get(uid=a_uid)
		else:
			account = DriveAccount.objects.get(uid=a_uid)

		account_id = a_uid
		email = account.email

		account.delete_account();

		data = {'success': True,
				'account_id': account_id,
				'email': email}
	except:
		data = {'success': False}

	return HttpResponse(json.dumps(data), content_type="application/json")


def upload(request, service=None, a_uid=None, path=None):
	
	user = request.user
	f = request.FILES['file']
	file_name = f.name

	if service == None:

		dropbox_accounts = DropboxAccount.objects.filter(user=user)
		drive_accounts = DriveAccount.objects.filter(user=user)
		accounts = list(chain(dropbox_accounts, drive_accounts))
		accounts.sort(key=lambda x: x.get_free_space(), reverse=True)

		# Uploads the file to the account with more free space
		account = accounts[0]
	else:
		if service == "dropbox":
			account = DropboxAccount.objects.get(uid=a_uid)
		elif service == "google-drive":
			account = DriveAccount.objects.get(uid=a_uid)

	account.upload_file(f, path)

	return HttpResponse()






