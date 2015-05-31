from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^/$', 'mwc_api.views.display_api', name='display_api'),

    url(r'^/path/$', 'mwc_api.views.get_path', name='get_home'),
    url(r'/path/(?P<service>(dropbox|google-drive))/(?P<a_uid>\d{1,})/(?P<path>(.*))?/?$',\
        'mwc_api.views.get_path', name='get_path'),

    url(r'^/download/(?P<service>(dropbox|google-drive))/(?P<a_uid>\d{1,})/(?P<path>(.*))/?$', 'mwc_dropbox.views.download', name='download'),

    url(r'^/upload/$', 'mwc_api.views.upload', name='upload_to_home'),
    url(r'/upload/(?P<service>(dropbox|google-drive))/(?P<a_uid>\d{1,})/(?P<path>(.*))/?$',\
        'mwc_api.views.upload', name='upload_to_path'),

    url(r'/delete_account/(?P<service>(dropbox|google-drive))/(?P<a_uid>\d{1,})$',\
        'mwc_api.views.delete_account', name='delete_account'),
)