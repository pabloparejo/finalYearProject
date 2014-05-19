from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^/$', 'mwc_api.views.display_api'),
    url(r'/get_path/(?P<service>(dropbox|google-drive))/(?P<a_uid>\d{1,})/(?P<path>(.*))/?$',\
        'mwc_api.views.get_path', name='get_path'),

    url(r'/upload/demo/$', 'mwc_api.views.upload'),

    
)