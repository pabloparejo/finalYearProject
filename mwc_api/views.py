#encoding:utf-8
from django.shortcuts import render
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount, CredentialsModel

from apiclient.http import MediaInMemoryUpload
from apiclient.discovery import build

from dropbox.client import DropboxClient
from oauth2client.django_orm import CredentialsField

from itertools import chain

from django.http import HttpResponse

import json, httplib2

# Create your views here.

def display_api(request):
	return HttpResponse('hello')


def get_path(request, service, a_uid, path):
	if service == "dropbox":
		account = DropboxAccount.objects.get(uid=a_uid)
	else:
		account = DriveAccount.objects.get(uid=a_uid)

	if not path:
		path = "/"

	data = account.get_path(path)

	return HttpResponse(json.dumps(data), content_type="application/json")

def delete_account(request, service, a_uid):
	if service == "dropbox":
		account = DropboxAccount.objects.get(uid=a_uid)
	else:
		account = DriveAccount.objects.get(uid=a_uid)

	account.delete()

	return HttpResponseRedirect('/services')

def upload(request):

	f = request.FILES['file']
	file_name = f.name

	user = request.user
	dropbox_accounts = DropboxAccount.objects.filter(user=user)
	drive_accounts = DriveAccount.objects.filter(user=user)
	accounts = list(chain(dropbox_accounts, drive_accounts))
	accounts.sort(key=lambda x: x.get_free_space(), reverse=True)

	account = accounts[0]

	account.upload_file(f)

	return HttpResponse()








