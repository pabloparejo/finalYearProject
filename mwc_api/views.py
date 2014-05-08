from django.shortcuts import render
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount

from django.http import HttpResponse

import json

# Create your views here.


def get_path(request, service, s_id, path):
	if service == "dropbox":
		account = DropboxAccount.objects.get(uid=s_id)
	else:
		account = DriveAccount.objects.get(uid=s_id)

	if not path:
		path = "/"
	
	data = account.get_path(path)

	return HttpResponse(json.dumps(data), content_type="application/json")

