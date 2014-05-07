from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from .models import DriveAccount, CredentialsModel

import os, httplib2, json

from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

# --- Google Drive keys ---#
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'google_secrets.json')

FLOW = flow_from_clientsecrets(
	CLIENT_SECRETS,
	scope='https://www.googleapis.com/auth/drive',
	redirect_uri='http://127.0.0.1:8000/googledrive_added')

@login_required()
def auth_start (request):
	authorize_url = FLOW.step1_get_authorize_url()
	return HttpResponseRedirect(authorize_url)

@login_required()
def auth_finish(request):
	user = request.user
	credentials = FLOW.step2_exchange(request.REQUEST)
	storage = Storage(CredentialsModel, 'user', user, 'credential')
	#storage.put(credentials)

	http = httplib2.Http()
	http = credentials.authorize(http)
	drive_service = build('drive', 'v2', http=http)
	user_info = drive_service.about().get().execute()['user']
	client_email = user_info['emailAddress']
	uid = user_info['permissionId']
	display_name = user_info['displayName']

	try:
		formerAccount = DriveAccount.objects.get(uid=uid)
		formerCredential = 	CredentialsModel.objects.\
							get(drive_account=formerAccount).delete()
		storage.put(credentials)
		credentials = CredentialsModel.objects.filter(user=user)
		credentials = credentials.order_by('-id')[0]
		formerAccount.credentialsmodel_set.add(credentials)
		formerAccount.email = client_email
		formerAccount.display_name = display_name
		new_account = False
	except ObjectDoesNotExist:
		new_account = True
		storage.put(credentials)
		credentials = CredentialsModel.objects.filter(user=user)
		credentials = credentials.order_by('-id')[0]

		new_account = DriveAccount(	uid=uid, display_name=display_name,\
									email=client_email)
		user.driveaccount_set.add(new_account)
		new_account.save()
		new_account.credentialsmodel_set.add(credentials)

	service_added = 'Google Drive'
	auth_finished = True
	return render(request, 'new_service.html', locals())


def get_drive_data(user):
    listOfAccounts = DriveAccount.objects.filter(user=user)
    services = []
    if listOfAccounts:
        for account in listOfAccounts:
            services.append(account.get_path('/'))
        accountsAreActive = True
    else:
        accountsAreActive = False
        metadata_list = ""
        
    return services
@login_required()
def list_files(request):
    user = request.user
    services = get_drive_data(user)

    data = {"username": request.user.username.encode('utf-8'),
            "number_of_services": len(services),
            "total_size": "habria que ver esto",
            "used_size": "habria que ver esto",
            "services": services}
    obj = json.dumps(data)
    return render(request,'index.html', locals())




