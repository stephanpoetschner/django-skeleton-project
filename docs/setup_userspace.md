# Application-Setup in User-Space

## Environment

    $ echo "export PATH=$HOME/bin:$PATH" >> ~/.bashrc
    $ echo "export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
    $ source ~/.bashrc
    $ mkdir -p ~/tmp
    $ mkdir -p ~/src

Create folders interfacing with the environment

    # put your deployed applications here (tag by version)
    $ mkdir -p ~/deployments

    # may contain a index.html and more html/css/js-files
    # if existant frontend webserver will not proxy to the application
    # and instead serve the static page
    $ mkdir -p ~/maintenance

    # where the frontend-server will put its log-files
    $ mkdir -p ~/logs/frontend

    # where we will put our logfiles
    $ mkdir -p ~/logs/user

    # statically served by the frontend-server
    $ mkdir -p ~/public

    # server by frontend-server, if application sends specific http-response
    # uses XSendfile module (nginx: XSendfile, apache: mod_xsendfile)
    $ mkdir -p ~/protected

    # put your configuration files here
    $ mkdir -p ~/etc

## Python

    $ cd ~/src
    $ wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tgz
    $ tar xzvf Python-2.7.5.tgz
    $ cd Python-2.7.5
    $ ./configure --prefix=$HOME
    $ make
    $ make install
    $ python
    $ which python

## Python-Environment

    $ cd ~/src
    $ wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.0.tar.gz
    $ tar xzvf setuptools-1.0.tar.gz
    $ cd setuptools-1.0
    $ python setup.py install

    $ easy_install pip

    $ pip install virtualenv
    $ pip install virtualenvwrapper
    $ mkdir -p ~/.virtualenvs
    $ echo "" >> ~/.bashrc
    $ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
    $ echo "source $HOME/bin/virtualenvwrapper.sh" >> ~/.bashrc
    $ echo "" >> ~/.bashrc
    $ source ~/.bashrc


## (webfaction-specific) Python-Imaging-Library Setup

Note: If not using webfaction as a host, skip these steps.
Also prefer to use Pillow instead of PIL.

Get PIL

    $ cd ~/src
    $ wget http://effbot.org/media/downloads/PIL-1.1.7.tar.gz
    $ tar -xzvf PIL-1.1.7.tar.gz
    $ cd PIL-1.1.7

Edit setup.py

    TCL_ROOT = None
    JPEG_ROOT = '/usr/lib64','/usr/include'
    ZLIB_ROOT = '/lib64','/usr/include'
    TIFF_ROOT = None
    FREETYPE_ROOT = '/usr/lib64','/usr/include/freetype2/freetype'
    LCMS_ROOT = None

Build my PIL-version

    $ python setup.py build_ext -i

Install version to virtual-environment

    $ workon preview|live
    $ python setup.py install

# FAQ

## How-To restart the application-server (gunicorn)?

Login to server

    (local) $ ssh summitlynx@summitlynx.webfactional.com

Use supervisor to restart the gunicorn server.

    $ supervisorctl restart live
    or
    $ supervisorctl restart preview

## Where can I find the server-configuration files?

    (local) $ ssh summitlynx@summitlynx.webfactional.com
    $ cd ~summitlynx/etc/live
    or
    $ cd ~summitlynx/etc/preview

## But where is the frontend-server binding to port 80 and serving the media-files?

> Webfaction's NGINX frontend-servers are receiving all-requests first hand.
> See https://my.webfaction.com/websites
>
> Requests to webfaction servers are logged in `~summitlynx/logs/frontend/*`
>
> Requests passed trough to our application-server (gunicorn) can be found 
> at `~summitlynx/logs/user/gunicorn_*.log`

## What is supervisord for?

Spervisord is a daemon process watching over our application servers. If an 
application-server shuts-down, it will be automatically restartet.
You can manually access the supervisor console by calling `supervisorctl` at the server's console.

A cronjob (See `crontab -e` when logged in at the server) will ensure 
supervisor is running, just in case the server restarts or supervisor shuts 
down for some reason.

## Testing

There is basic testing for the `restapi` app (Postgres required). Run via:

    (local) $ python manage.py test restapi

Tests are grouped by topic. eg. to run just the checkin tests:

    (local) $ python manage.py test restapi.RestApiTests.test_checkin_functions

To use django-nose for testing, add this to the "test" section fo your local_settings.py:

    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


When using django-nose the tests can be run selectively like this:

    (local) $ python ./manage.py test restapi.tests:RestApiTests.test_checkin_functions
