# coding: utf-8
import sys, os

from fabric.api import *
from fabric import colors
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.contrib.console import confirm

from path import path

import settings

env.shell = "/bin/bash -li -c"

env.hosts = [ "root@wroot@myserver.com", ]
env.local_database_config = settings.DATABASES['default']


def reinit_database():
    local(u"dropdb %(NAME)s" % env.local_database_config)
    local(u"createdb --owner %(USER)s %(NAME)s" % env.local_database_config)

def reset():
    reinit_database()
    local('./manage.py clean_pyc')
    local('./manage.py syncdb --noinput')
    local('./manage.py migrate --noinput')

