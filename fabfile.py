from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['root@myserver.com']
env.shell = "/bin/bash -li -c"

def deploy():
    pass

def init_data():
    local('./manage.py runscript live_auth live_sites')

def init_testdata():
    #local('./manage.py runscript test_auth')
    pass

def reset():
    local('rm ./dev.db || true')
    local('./manage.py clean_pyc')
    local('./manage.py syncdb --noinput')
    init_data()
    init_testdata()

