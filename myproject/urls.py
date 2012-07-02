# coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('core.urls')),
    (r'^account/', include('profiles.urls')),
    (r'^', include('auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.MEDIA_SERVE:
    urlpatterns += patterns(
        '',

        # for development without apache
        (r'^assets/uploaded/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
