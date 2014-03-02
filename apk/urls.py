from django.conf.urls import patterns, url

from apkdissect.apk import views

urlpatterns = patterns('',
    url(r'^showclass/(?P<class_id>\d+)$', views.showclass, name='showclass'),
    url(r'^showapk/(?P<apk_id>\d+)$', views.showapk, name='showapk')
)
