#encoding:utf-8
from django.shortcuts import render

import json
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount

# Create your views here.

def home(request):
	drive = DriveAccount()
	dropbox1 = DropboxAccount()
	dropbox2 = DropboxAccount()

	services = [drive.get_path('/'), dropbox1.get_path('/'), dropbox2.get_path('/')]

	data = {"username": "request.user",
			"number_of_services": len(services),
			"total_size": "habria que ver esto",
			"used_size": "habria que ver esto",
			"services": services}

	obj = json.dumps(data)
	page_title = "home"

	return render(request, 'index.html', locals())