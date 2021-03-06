import os
import socket

from ConfigParser import RawConfigParser


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('George Hamilton', 'gmh04@netscape.net'),
)

MANAGERS = ADMINS
PROJECT_ROOT = os.path.dirname(__file__)

hostname = socket.gethostname()

def is_live():
    return hostname == 'ip-10-227-51-57'

config = RawConfigParser()

if is_live():
    config_file = '/home/gmh04/.news/config.ini'
else:
    config_file = '/home/ghamilt2/.news/config.ini'

config.read(config_file)

if is_live():
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'news',
        'USER': 'gmh04',
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.sep.join((PROJECT_ROOT, 'news.db')),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
    }
}

DATABASE_OPTIONS = {
    "autocommit": True,
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.sep.join((PROJECT_ROOT, 'static'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#nbc$57(00i@bl7mlaohz7wun@v*!=7hq^nezm718f3%2e5%xo'

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
)

ROOT_URLCONF = 'newssrv.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.sep.join((PROJECT_ROOT, 'templates')),
    os.sep.join((PROJECT_ROOT, 'feeds', 'templates'))
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'registration',
    'django_countries',
    'newssrv.feeds',
)


STATIC_ROOT = os.sep.join((PROJECT_ROOT, 'static'))
STATICFILES_DIRS = (
    STATIC_ROOT,
)
STATIC_URL = '/static'
ICONS_ROOT = os.sep.join((STATIC_ROOT, 'icons'))

# smtp settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ghamilt2@gmail.com'
EMAIL_HOST_PASSWORD = config.get('smtp', 'SMTP_PASSWORD')
EMAIL_USE_TLS = True

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = 'http://localhost:1314'
