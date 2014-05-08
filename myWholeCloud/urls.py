from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myWholeCloud.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.home'),
    url(r'^login/$', 'main.views.user_login', \
		name="login"),
    url(r'^register/$', 'main.views.new_user', \
		name="new_user"),
    url(r'^logout/$', 'main.views.user_logout', \
		name="logout"),

    url(r'^add_account/$', 'main.views.new_service'),
    url(r'^api/get_path/(?P<service>(dropbox|google-drive))/(?P<s_id>\d{1,})/(?P<path>(.*))/$',\
         'mwc_api.views.get_path', name="get_path"),

    url(r'^dropbox/$', 'mwc_dropbox.views.list_files'),
    url(r'^add_dropbox/$', 'mwc_dropbox.views.auth_start'),
    url(r'^dropbox_added/$', 'mwc_dropbox.views.auth_finish'),

    url(r'^add_drive/$', 'mwc_drive.views.auth_start'),
    url(r'^googledrive_added/$', 'mwc_drive.views.auth_finish'),
    url(r'^drive/$', 'mwc_drive.views.list_files'),
)
