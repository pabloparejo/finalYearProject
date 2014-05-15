#encoding:utf-8
from django.shortcuts import render
from mwc_dropbox.models import DropboxAccount
from mwc_drive.models import DriveAccount, CredentialsModel

from apiclient.http import MediaInMemoryUpload
from apiclient.discovery import build

from dropbox.client import DropboxClient
from oauth2client.django_orm import CredentialsField



from django.http import HttpResponse

import json, httplib2

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

	f = request.FILES['file']
	file_name = f.name
	print "file"

	# DROPBOX
	# account = DropboxAccount.objects.get(uid=41254046)
	# client = DropboxClient(account.token)
	# client.put_file('/other.js', f, overwrite=True, parent_rev=None)

	# DRIVE
	account = DriveAccount.objects.get(uid=946419211659158232)
	credentials_model = CredentialsModel.objects.get(drive_account=account)
	credentials = credentials_model.credential
	http = httplib2.Http()
	http = credentials.authorize(http)

	drive_service = build('drive', 'v2', http=http)

	media_body = MediaInMemoryUpload(file_name, mimetype='text/plain', resumable=True)
	body = {'description': 'A test document',
			'mimeType': 'text/plain',
			'title': file_name
		}

	f = drive_service.files().insert(body=body, media_body=media_body).execute()
	
	return HttpResponse()








