#encoding:utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

import json

from dropbox_keys import app_key, app_secret
from mwc_dropbox.models import DropboxAccount
from dropbox.client import DropboxClient, DropboxOAuth2Flow

from django.contrib.auth.decorators import login_required

def download(request, service, a_uid, path):
    user=request.user
    service = get_object_or_404(DropboxAccount, uid=a_uid)

    document = service.view_file(path)

    filename = path.split('/')[-1]

    response = HttpResponse(content_type=document.get('content_type'))
    response['Content-Disposition'] = 'filename="'+filename+'"'

    response.write(document.get('contents'))

    return response


def get_dropbox_data(user):
    listOfAccounts = DropboxAccount.objects.filter(user=user)
    services = []
    if listOfAccounts:
        for account in listOfAccounts:
            services.append(account.get_path('/'))
        accountsAreActive = True
    else:
        accountsAreActive = False
        metadata_list = ""
        
    return services


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

def get_auth(web_app_session):

    redirect_uri = 'http://127.0.0.1:8000/dropbox_added'
    return DropboxOAuth2Flow (  app_key, app_secret, redirect_uri,\
                                web_app_session, 'dropbox-auth-csrf-token')

@login_required()
def auth_start(request):
    authorize_url = get_auth(request.session).start()
    return HttpResponseRedirect(authorize_url)
    
@login_required()
def auth_finish(request):
    try:
        access_token, user_id, url_state = get_auth(request.session).finish(request.GET)
        client = DropboxClient(access_token).account_info()
        user = request.user
        client_email = client.get('email', '')
        uid = client.get('uid', '')
        name = client.get('display_name', '')
        
        try:
            formerAccount = DropboxAccount.objects.get(uid=uid)
            formerAccount.token = access_token
            formerAccount.display_name = name
            formerAccount.email = client_email
            formerAccount.save()
            new_account = False
        except ObjectDoesNotExist:
            new_account = True
            account = user.dropboxaccount_set.create(   uid=uid, 
                                                        token=access_token,
                                                        email=client_email,
                                                        display_name=name)

        response = HttpResponseRedirect('/services')
        response.set_cookie('service_added', 'dropbox', path="/")
        response.set_cookie('new_account', new_account, path="/")
        response.set_cookie('account_uid', uid, path="/")

        return response

    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
        info = 'error404'
        return render(request,'dropbox.html', {'info':info})
    except DropboxOAuth2Flow.BadStateException, e:
        return HttpResponseRedirect('/add_dropbox')
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