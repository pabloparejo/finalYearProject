from django.shortcuts import render
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount
from dropbox.client import DropboxClient

from django.http import HttpResponse

import json

# Create your views here.


def get_path(request, service, a_uid, path):
	if service == "dropbox":
		account = DropboxAccount.objects.get(uid=a_uid)
	else:
		account = DriveAccount.objects.get(uid=a_uid)

	if not path:
		path = "/"

	data = account.get_path(path)

	return HttpResponse(json.dumps(data), content_type="application/json")

# ONLY FOR TEST PURPOSES -- REMOVE THIS VIEW
def upload_demo(request):
	account = DropboxAccount.objects.get(uid=41254046)
	client = DropboxClient(account.token)

	f = request.FILES['file']

	client.put_file('/other.js', f, overwrite=True, parent_rev=None)

	return HttpResponse()