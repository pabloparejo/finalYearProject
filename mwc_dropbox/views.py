#encoding:utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect

import json

from dropbox_keys import app_key, app_secret
from mwc_dropbox.models import DropboxAccount
from dropbox.client import DropboxClient, DropboxOAuth2Flow

from django.contrib.auth.decorators import login_required

def serve_file(request, service_email, path):
    user=request.user
    print path
    service = service_account.objects.get(service='dropbox',
                                          user=user,
                                          service_email__startswith=service_email)
    sharedFile = DropboxClient(service.service_token).share(path, short_url=False)
    downloadLink = sharedFile['url'].replace('www.dropbox.com', 'dl.dropboxusercontent.com', 1)
    print downloadLink
    return HttpResponseRedirect(downloadLink)

@login_required()
def list_files(request):
    user = request.user
    listOfAccounts = DropboxAccount.objects.filter(user=user)
    services = []
    if listOfAccounts:
        for account in listOfAccounts:
            services.append(account.get_path('/'))
        accountsAreActive = True
    else:
        accountsAreActive = False
        metadata_list = ""

    data = {"username": request.user.username.encode('utf-8'),
            "number_of_services": len(services),
            "total_size": "habria que ver esto",
            "used_size": "habria que ver esto",
            "services": services}
    obj = json.dumps(data)
    return render(request,'files.html', locals())


def get_auth(web_app_session):

    redirect_uri = 'http://127.0.0.1:8000/dropbox_added'
    return DropboxOAuth2Flow (  app_key, app_secret, redirect_uri,\
                                web_app_session, 'dropbox-auth-csrf-token')

@login_required()
def auth_start(request):
    authorize_url = get_auth(request.session).start()
    return HttpResponseRedirect(authorize_url)

def new_account(user, dropbox_client, token):
    client_email = dropbox_client.account_info()['email']
    client_id = dropbox_client.account_info()['uid']
    display_name = dropbox_client.account_info()['display_name']
    account = user.dropboxaccount_set.create(   uid=client_id,
                                                token=token,
                                                email=client_email,
                                                display_name=display_name)
    account.save()
    
    return account
    
@login_required()
def auth_finish(request):
    try:
        access_token, user_id, url_state = get_dropbox_auth(request.session).finish(request.GET)
        client = DropboxClient(access_token)
        user = request.user
        client_email = client.account_info()['email']
        client_id = client.account_info()['uid']
        display_name = client.account_info()['display_name']

        formerAccounts = DropboxAccount.objects.filter(user=user)
        accountIsUsed = False
        if formerAccounts:
            for account in formerAccounts:
                print account.uid
                print client_id
                if (account.uid== client_id):
                    account.service_token = access_token
                    account.service_token = client_email
                    account.service_token = display_name
                    account.save()
                    subtitle = "La cuenta %s ya estaba incluida" , client_email 
                    accountIsUsed = True
        
        if (not accountIsUsed) or (not formerAccounts):
            1/0
            new_account = new_account(user, client, access_token)
            subtitle = "Servicio nuevo añadido: %s" , new_account.email
        return HttpResponseRedirect('/')
    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
        info = 'error404'
        return render(request,'dropbox.html', {'info':info})
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        info = 'Start Flow again'
        return render(request,'dropbox.html', {'info':info})
    except DropboxOAuth2Flow.CsrfException, e:
        info = 'CSRF ERROR'
        return render(request,'dropbox.html', {'info':info})
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException, e:
        info = 'NOT APPROVED ERROR'
        return render(request,'dropbox.html', {'info':info})
        raise e
    except DropboxOAuth2Flow.ProviderException, e:
        info = 'PROVIDER EXC ERROR'
        return render(request,'dropbox.html', {'info':info})
        raise e