# MyProject

## Pre-Requirements

1.  Install python 2.7, setuptools and virtualenvwrapper

        $ sudo apt-get install python2.7 python-dev python-setuptools virtualenvwrapper

2.  Install postgreSQL

        $ sudo apt-get install postgresql-server-dev-9.1

3.  Create database user

        $ sudo su - postgres                 # Switch to user postgres
        $ createuser -s -E -P <my_db_user>   # Create database user named 'my_db_user' (superuser, encrypted password, password prompt)

4.  Allow user to connect and restart postgresql
    * Edit `/etc/postgresql/9.1/main/pg_hba.conf`
    * Add the following line (so your user is allowed to connect from localhost) to `/etc/postgresql/9.1/main/pg_hba.conf`
      IMPORTANT: Do not blindly copy these lines at the end of the file. Rather copy it into the appropriate section saying: `# Put your actual configuration here`

          local my_db_user my_db_user password

      … or on your development machine

          local   all         all         trust
          host    all         all         127.0.0.1/32          trust

    * Restart postgres: `/etc/init.d/postgresql restart`
    * Log user 'postgres' out: `logout`

5.  Install PIL dependencies

        $ sudo apt-get install libjpeg8 libjpeg8-dev libfreetype6 libfreetype6-dev zlib1g-dev


    Ubuntu has it's libraries where PIL does not find it, so you will have to make some link to them so PIL can be installed:

        $ sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
        $ sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
        $ sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

    (see also http://jj.isgeek.net/2011/09/install-pil-with-jpeg-support-on-ubuntu-oneiric-64bits/)


## Fork from skeleton project

1.  Make, enter and activate a virtualenv:

        $ mkvirtualenv <my_project> -p python2.7
        New python executable in <my_project>/bin/python
        Installing setuptools............done.
        $ workon <my_project>

2.  Clone this repo into a sub-directory of the new virtualenv:

        $ git clone 'git://github.com/stephanpoetschner/django-skeleton-project.git' <project_folder>
        $ cd <project_folder>/

        $ git mv <my_project> <custom_project_name>

        # Remove .empty files, used to make Hg track otherwise-empty dirs.
        $ find . -name '.empty' -exec rm {} \;

        # edit or clear .gitignore
        $ vi .gitignore
        $ echo > .gitignore

3.  Remove the pointer to the GitHub project:

        $ git config --unset remote.origin.url

    Later you’ll probably want to re-add this configuration with a pointer to
    your upstream repo. You can do that with the following command:

        $ git config remote.origin.url 'git@github.com:USERNAME/PROJECT.git'

4.  Install base requirements

        $ easy_install pip
        $ pip install -r requirements/base.txt

5.  Ensure current (working) version numbers are documented

        $ pip freeze > requirements/base.txt

6.  Install the project specific requirements:

        $ pip install -r requirements/project.txt

    As you edit your `requirements/project.txt` file, you can run that last command again;
    `pip` will realise which packages you’ve added and will ignore those already
    installed.

6.  Delete this subsection of the `README.md` file

7.  Commit changes to new repository

        $ git commit -a


## Installation

1.  Make, enter and activate a virtualenv:

        $ mkvirtualenv <my_project> -p python2.7
        New python executable in <my_project>/bin/python
        Installing setuptools............done.
        $ workon <my_project>

2.  Install requirements (pre-requirement: python-setuptools)

        $ easy_install pip
        $ pip install -r requirements.txt

3.  Copy `localsettings.py.skel` to `localsettings.py`

4.  Go through the following files, editing as necessary:

   * `localsettings.py`
   * `settings.py`
     * Update SECRET_KEY (call `./manage.py generate_secret_key`)

5.  Create initial postgres-database

        $ createdb --owner <my_db_user> <my_database>


## Initializing the local development environment

1.  Sync the database with the apps model

        $ fab reset

        or

        $ ./manage.py syncdb

2.  Run the test-suite

        $ ./manage.py test

3.  Add data

    * add test data or …

        $ ./manage.py loaddata apps/profiles/fixtures/profiles.json
        $ …

    * … import data from db2 system

        $ ./manage.py db2sync

4.  Start the devserver

        $ ./manage.py runserver
