# coding: utf-8
import sys, os

from fabric.api import *
from fabric import colors
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.contrib.console import confirm

import shutil

from path import path as _path

import settings

env.shell = "/bin/bash -li -c"

env.hosts = [ "root@myserver.com", ]
env.local_database_config = settings.DATABASES['default']

env.remote_root = _path("/home/my_webfaction_user/webapps/")
env.remote_virtualenv = _path("/home/my_webfaction_user/.virtualenvs/")

env.stages = {
    #"live": [ "live", ],
    "preview": [ "preview", ],
}
env.local_source = _path(__file__).abspath().realpath().dirname()
env.local_project_root, src_folder = env.local_source.splitpath()

env.deploy_dir = env.local_project_root / "deploy" / ""
env.deploy_src_dir = env.deploy_dir / "src" / ""



def reinit_database():
    local(u"dropdb %(NAME)s" % env.local_database_config)
    local(u"createdb --owner %(USER)s %(NAME)s" % env.local_database_config)

def reset():
    reinit_database()
    local('./manage.py clean_pyc')
    local('./manage.py syncdb --noinput')
    local('./manage.py migrate --noinput')


def deploy(stage="preview"):
    if stage not in env.stages.keys():
        abort(colors.red(u"Selected stage not valid. Select from (%s)" % \
                         ", ".join(env.stages.keys())))

    if stage == "live":
        if not confirm(
            colors.red(u"Are you sure you want to update the live environment?"),
            default=False
            ):
            abort(u"Aborting update process.")

    puts(u"Deploying to %s" % stage)
    prepare_export()

    puts(u"Syncing project folders")
    rsync_project(env.remote_root / stage, env.deploy_src_dir)

    puts(u"Cleaning up: removing svn export")
    shutil.rmtree(env.deploy_dir)

    venv_path = env.remote_virtualenv / stage / 'bin'
    with (cd(env.remote_root / stage)):
        puts(u"Syncing requirements")
        run('%s/pip install -r requirements/project.txt' % venv_path)

        puts(u"Running syncdb")
        run('%s/python manage.py syncdb' % venv_path)

        puts(u"Running database migrations via South")
        run('%s/python manage.py migrate' % venv_path)

    puts(u"Restarting services")
    for process_name in env.stages[stage]:
        run("supervisorctl restart %s" % process_name)


def prepare_export():
    local(u"git clone %s %s" % (env.local_project_root, env.deploy_dir))
    local(u"cd %s && git log > %s" % (env.local_project_root,
                                      env.deploy_src_dir / u'release.txt'))


def import_database(stage="live"):
    if stage not in env.stages:
        abort(colors.red(u"Selected stage not valid. Select from (%s)" % \
                         ", ".join(env.stages)))
    remote_file = env.remote_root / stage / "dbdump.sql"
    local_file = env.local_source / "dbdump.sql"
    run("pg_dump immovate_%s -U immovate_%s > %s" % (stage, stage, remote_file))
    get(remote_file, local_file)

    #reinit()
    local("python manage.py dbshell < %s" % local_file)

def import_assets(stage="live"):
    if stage not in env.stages.keys():
        abort(colors.red(u"Selected stage not valid. Select from (%s)" % \
                         ", ".join(env.stages.keys())))
    remote_assets = env.remote_root / stage / "assets" / "uploaded" / ""
    local_assets = env.SOURCE_ROOT / "assets" / "uploaded" / ""
    local("rsync -avz %s:%s %s" % (env.host_string,
                                   remote_assets,
                                   local_assets))
