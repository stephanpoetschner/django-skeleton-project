# coding: utf-8
from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend

class EmailModelBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
