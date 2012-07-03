# coding: utf-8
from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
)

if settings.ENABLE_ERROR_VIEWS:
    urlpatterns += patterns('',
        url(r'^500/$', error_500, name='error_500'),
        url(r'^404/$', error_404, name='error_404'),
    )
