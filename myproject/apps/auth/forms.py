# -*- coding: utf-8 -*-
import hashlib

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator


class EmailAuthenticationForm(auth.forms.AuthenticationForm):
    email = forms.EmailField(label=_(u"Deine Emailadresse"),
                             max_length=75)

    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'email', self.fields.pop('email'))
        del self.fields['username']

    def clean(self):
        given_email = self.cleaned_data.get(u'email')
        given_password = self.cleaned_data.get(u'password')

        if given_email and given_password:
            self.user_cache = auth.authenticate(email=given_email,
                                                password=given_password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data


class SetPasswordDuringAccountInitForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordDuringAccountInitForm, self).__init__(*args, **kwargs)

    def is_valid(self, *args, **kwargs):
        retval = super(SetPasswordDuringAccountInitForm, self).is_valid()
        if retval == True:

            email_template_name = 'auth/welcome_message_email.txt'
            c = { 'user': self.user, }
            email_message = loader.render_to_string(email_template_name, c)

            send_mail(subject=_('Willkommen'),
                      message=email_message,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[ self.user.email, ],)
        return retval