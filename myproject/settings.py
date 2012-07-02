# -*- coding: utf-8 -*-
import posixpath
from path import path
import sys

from django.core.urlresolvers import reverse_lazy

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = False


PROJECT_ROOT = path(__file__).abspath().realpath().dirname()
sys.path.insert(0, PROJECT_ROOT / "apps")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'woj)6x+lm$yz(bxh746fz9z064=iecd(v)=qc7fxij$=0e2mdw'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT / 'dev.db',
    }
}

SITE_ID = 1
DEFAULT_HTTP_PROTOCOL = "http"


PAGINATION_DEFAULT_PAGINATION = 25
PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_DEFAULT_ORPHANS = 0

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-AT'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

ugettext = lambda s: s # rather hackish but suggested by...
## ... http://docs.djangoproject.com/en/1.1/topics/i18n/deployment/#how-django-discovers-language-preference
## to prevent circular dependancies
LANGUAGES = (
    #('en', ugettext('English')),
    ('de', ugettext('German')),
)

MEDIA_ROOT = PROJECT_ROOT / 'assets' / 'uploaded' / '' # ensure trailing slash
MEDIA_URL = '/assets/uploaded/'

STATIC_ROOT = PROJECT_ROOT / "assets" / "static" / '' # ensure trailing slash
STATIC_URL = '/assets/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT / "static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',

    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',

    'pagination.middleware.PaginationMiddleware',
)


ROOT_URLCONF = 'urls'

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = PROJECT_ROOT / '..' / 'debug-mails'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'auth.backends.EmailModelBackend',
)
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

TEMPLATE_DIRS = (
    PROJECT_ROOT / "templates",
)

CONTEXT_SETTINGS = (
    "DEBUG",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    "core.context_processors.global_settings",
    "core.context_processors.site_url",

)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.messages',

    #external
    'compressor',
    'django_extensions',
    'pagination',
    'easy_thumbnails',
    'uni_form',
    'south',

    #internal
    'core',
    'auth',
    'profiles',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from localsettings import *
except ImportError:
    pass
