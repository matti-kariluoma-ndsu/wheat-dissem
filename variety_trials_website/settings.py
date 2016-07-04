#!/usr/bin/env python
# coding: ascii

"""
Django settings for variety_trials_website project.

:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
import os
try:
	from . import secrets # a file not kept in the code repository!
except ImportError:
	print("You haven't created a 'secrets.py' file. Please consult the README")
	import sys
	sys.exit(1)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

BASE_URL = '/'
LOGIN_URL = BASE_URL + 'accounts/login/'

NOPASSWORD_LOGIN_CODE_TIMEOUT = 60*5 # five minutes

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60*60*1 # one hour

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'donotreply.whip@gmail.com'
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = True

NOPASSWORD_LOGIN_EMAIL_SUBJECT = 'Your Login for WHIP'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, 'sqlite.db'), # Or path to database file if using sqlite3.
   }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/tmp/whip/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '' # don't serve user-uploaded files

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common/static'),
    os.path.join(BASE_DIR, 'variety_trials_data/static/'),
)

# URL prefix for all links, not automaticcally appended, though.
HOME_URL = ''

# Where are the R libraries?
R_LIBRARY = os.path.join(BASE_DIR, 'R/library')

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zvzu%y8rvs#g42qiwc-9^_hm@-uu7y^6tkoh%w%5^rnb$ay@gd'

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

USE_ETAGS=True # see CommonMiddleWare

MIDDLEWARE_CLASSES = (
		'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'variety_trials_website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'variety_trials_website.wsgi.application'

TEMPLATE_DIRS = (
		'variety_trials_data/templates/',
		'variety_trials_data/templatetags/'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'variety_trials_data',
    'upload_spreadsheet',
    'nopasswordauth',
    'nopassword',
    'common',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
)

AUTHENTICATION_BACKENDS = (
    'nopassword.backends.email.EmailBackend',
)

AUTH_USER_MODEL = 'nopasswordauth.NoPasswordUser'

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

CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'LOCATION': '/tmp/wheat_dissem_cache',
        #'TIMEOUT': 300,
    }
}


