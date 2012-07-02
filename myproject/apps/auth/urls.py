# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.views import *
from auth.forms import EmailAuthenticationForm, SetPasswordDuringAccountInitForm

urlpatterns = patterns(
    '',

    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^login/$', login,
        kwargs={
            'template_name': 'auth/login.html',
            'authentication_form': EmailAuthenticationForm,
            },
        name='login'),

    url(r'^passwort-aendern/$', password_change,
        kwargs={
            'template_name': 'auth/password_change.html',
            },
        name='password_change'),
    url(r'^passwort-aendern/ok/$', password_change_done,
        kwargs={
            'template_name': 'auth/password_change_done.html',
            },
        ),

    url(r'^passwort-vergessen/$', password_reset,
        kwargs={
            'template_name': 'auth/password_reset.html',
            'email_template_name': 'auth/password_reset_email.html',
            },
        name='password_reset'),
    url(r'^passwort-zuruecksetzen/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        kwargs={
            'post_reset_redirect': reverse_lazy('login'),
            'template_name': 'auth/password_reset_confirm.html',
        },
        name='password_reset_confirm'),
    url(r'^passwort-vergessen/ok/$', password_reset_done,
        kwargs={
            'template_name': 'auth/password_reset_done.html',
            },
        ),
)