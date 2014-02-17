from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'androidforensics.views.home', name='home'),
    #url(r'^apk/', include('apk.urls')),
    url(r'^$', 'apk.views.apkindex', name='apkindex'),
    url(r'^showclass/(?P<class_id>\d+)$', 'apk.views.showclass', name='showclass'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
