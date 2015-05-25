from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'main.views.home'),
    url(r'^login/$', 'main.views.user_login', \
		name="login"),
    url(r'^register/$', 'main.views.new_user', \
		name="new_user"),
    url(r'^logout/$', 'main.views.user_logout', \
		name="logout"),

    url(r'^api', include('mwc_api.urls')),

    url(r'^services/$', 'main.views.show_services'),

    url(r'^add_dropbox/$', 'mwc_dropbox.views.auth_start'),
    url(r'^dropbox_added/$', 'mwc_dropbox.views.auth_finish'),

    url(r'add_account/(?P<service>(dropbox|google-drive))/$',\
         'main.views.add_account', name='add_account'),

    url(r'^add_drive/$', 'mwc_drive.views.auth_start'),
    url(r'^googledrive_added/$', 'mwc_drive.views.auth_finish'),
)
