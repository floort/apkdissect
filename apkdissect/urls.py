from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'androidforensics.views.home', name='home'),
    #url(r'^apk/', include('apk.urls')),
    url(r'^$', 'apk.views.index', name='index'),
    url(r'^apk/(?P<apk_id>\d+)/classes_menu.json$', 'apk.views.classes_menu_json', name='classes_menu_json'),
    url(r'^apk/(?P<apk_id>\d+)/source.zip$', 'apk.views.classes_zip', name='classes_zip'),
    url(r'^apk/menu.json$', 'apk.views.menu_json', name='menu_json'),
    url(r'^$', 'apk.views.appindex', name='appindex'),
    url(r'^showclass/(?P<class_id>\d+)$', 'apk.views.showclass', name='showclass'),
    url(r'^showapk/(?P<apk_id>\d+)$', 'apk.views.showapk', name='showapk'),
    url(r'^dissect/(?P<apk_id>\d+)$', 'apk.views.dissect', name='dissect'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
