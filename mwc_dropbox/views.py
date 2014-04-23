from django.shortcuts import render

from dropbox_keys import app_key, app_secret


def get_dropbox_auth(web_app_session):

    redirect_uri = 'http://127.0.0.1:8000/dropbox_added'
    return DropboxOAuth2Flow (  app_key, app_secret, redirect_uri,\
                                web_app_session, 'dropbox-auth-csrf-token')


def dropbox_path(request, service_email, path):
    user=request.user
    print path
    service = service_account.objects.get(service='dropbox',
                                          user=user,
                                          service_email__startswith=service_email)
    client = DropboxClient(service.service_token)
    metadata_list = client.metadata(path)['contents']
    for element in metadata_list:
                if element['is_dir']:
                    element['url'] = ('/' + service.service + '/'
                                  + service.service_email.split('@')[0]
                                  + element['path'])
                else:
                    element['url'] = ('/file/' + service.service + '/'
                                  + service.service_email.split('@')[0]
                                  + element['path'])
    accountsAreActive = True
    listOfAccounts = [service.service_email]
    return render(request,  'dropbox.html', locals())
    

def serve_dropbox_file(request, service_email, path):
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
def dropbox_files(request):
    user = request.user
    listOfServices = service_account.objects.filter(user=user)
    listOfAccounts = []
    if listOfServices:
        metadata_list = []
        for service in listOfServices:
            client = DropboxClient(service.service_token)
            metadata_list += client.metadata('/')['contents']
            for element in metadata_list:
                if element['is_dir']:
                    element['url'] = ('/' + service.service + '/'
                                  + service.service_email.split('@')[0]
                                  + element['path'])
                else:
                    element['url'] = ('/file/' + service.service + '/'
                                  + service.service_email.split('@')[0]
                                  + element['path'])
            listOfAccounts.append(service.service_email)
        accountsAreActive = True
    else:
        accountsAreActive = False
        metadata_list = ""
    print listOfAccounts
    return render(request,'dropbox.html', locals())

    
@login_required()
def dropbox_auth_start(request):
    authorize_url = get_dropbox_auth(request.session).start()
    return HttpResponseRedirect(authorize_url)

def new_dropbox_service(user, dropbox_client, token):
    client_email = dropbox_client.account_info()['email']
    client_id = dropbox_client.account_info()['uid']
    
    service = user.service_account_set.create(service="dropbox",
                                              service_token=token,
                                              service_email=client_email,
                                              service_user_id=client_id)
    service.save()
    
    return service
    
@login_required(login_url='/login/')
def dropbox_auth_finish(request):
    try:
        access_token, user_id, url_state = get_dropbox_auth(request.session).finish(request.GET)
        client = DropboxClient(access_token)
        user = request.user
        formerServices = service_account.objects.filter(user=user)
        accountIsUsed = False
        if formerServices:
            for service in formerServices:
                if (service.service_email == client.account_info()['email']):
                    service.service_token = access_token
                    #service.save()
                    subtitle = "La cuenta " + service.service_email + " ya estaba incluida"
                    accountIsUsed = True
                    
        if (not accountIsUsed) or (not formerServices):
            new_service = new_dropbox_service(user, client, access_token)
            subtitle = "Servicio nuevo añadido: %s" , new_service.service_email
        return HttpResponseRedirect('/dropbox')
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