# coding: utf-8
import json

from django.conf import settings
from django.core import serializers
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from datetime import datetime

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name=u'profile')

    # Other fields here
    # …

    @property
    def email(self):
        return self.user.email

    @property
    def is_active(self):
        return self.user.is_active

    def __unicode__(self):
        return u", ".join(filter(None, [ unicode(self.user),
                                         self.user.email, ]))


# automatically adding UserProfile to User-instance, if created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
