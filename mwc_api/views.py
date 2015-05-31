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
from myWholeCloud.settings import SITE_URL
from django.core.urlresolvers import reverse

# Create your views here.

def format_url(urls, url_name, method, url_args=None):
	if not urls.has_key(url_name):
		urls[url_name] = []

	url_dict = {"method": method,
				"url": SITE_URL + reverse(url_name, kwargs=url_args)[1:]}

	if url_args and url_args.has_key("a_uid"):
		url_dict["a_uid"] = url_args["a_uid"]
		url_dict["service_class"] = url_args["service"]

	urls[url_name].append(url_dict)

def display_api(request):
	user = request.user

	dropbox_services = DropboxAccount.objects.filter(user=user)
	drive_services = DriveAccount.objects.filter(user=user)

	urls = {}

	format_url(urls, 'display_api', 'GET')
	format_url(urls, 'get_home', 'GET')
	format_url(urls, 'upload_to_home', 'POST')

	for service in dropbox_services:
		format_url(urls, 'get_path', 'GET', {"service": service.service_class, "a_uid": service.uid, "path": ""})
		format_url(urls, 'delete_account', 'POST', {"service": service.service_class, "a_uid": service.uid})
		format_url(urls, 'upload_to_path', 'POST', {"service": service.service_class, "a_uid": service.uid, "path": ""})

	for service in drive_services:
		format_url(urls, 'get_path', 'GET', {"service": service.service_class, "a_uid": service.uid, "path": ""})
		format_url(urls, 'delete_account', 'POST', {"service": service.service_class, "a_uid": service.uid})
		format_url(urls, 'upload_to_path', 'POST', {"service": service.service_class, "a_uid": service.uid, "path": ""})



	return HttpResponse(json.dumps(urls), content_type="application/json")

def get_user_home(request):
	user = request.user
	dropbox_services = DropboxAccount.objects.filter(user=user)
	drive_services = DriveAccount.objects.filter(user=user)
	services = []
	for service in dropbox_services:
		services.append(service.get_path('/'))

	for service in drive_services:
		services.append(service.get_path('/'))

	data = {"username": user.username,
			"services": services}

	return data

def get_path(request, service=None, a_uid=None, path=None):
	user = request.user
	if service == None:
		data = get_user_home(request)
	else:
		if path == "": #Path is passed by view get_path
			path = "/"

		if service == "dropbox":
			account = DropboxAccount.objects.get(uid=a_uid)
		elif service == "google-drive":
			account = DriveAccount.objects.get(uid=a_uid)

		data = {"username": user.username,
				"services": [account.get_path(path)]}

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






