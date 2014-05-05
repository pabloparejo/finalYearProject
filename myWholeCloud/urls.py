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
    url(r'^dropbox/$', 'mwc_dropbox.views.list_files'),
    url(r'^add_dropbox/$', 'mwc_dropbox.views.auth_start'),
    url(r'^dropbox_added/$', 'mwc_dropbox.views.auth_finish'),
)
