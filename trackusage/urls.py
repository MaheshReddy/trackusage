from django.conf.urls import patterns, include, url
from django.contrib import admin

#urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'trackusage.views.home', name='home'),
#    url(r'^track_process/', include('track_process.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns = patterns('',
    url(r'^track_process/', include('track_process.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
