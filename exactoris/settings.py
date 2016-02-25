"""
Django settings for exactoris project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import basename
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_NAME = basename(BASE_DIR)

ADMINS = ('Erik', 'e.ocakovskis@gmail.com')

try:
  SECRET_KEY
except NameError:
  SECRET_FILE = os.path.join(BASE_DIR, '.secret')
  try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
  except OSError:
    import random
    import string
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation) for i in range(100)])
    secret_file = open(SECRET_FILE, 'w')
    secret_file.write(SECRET_KEY)
    secret_file.close()
    os.chmod(SECRET_FILE, 0o400)

DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))

if os.environ['DJANGO_ALLOWED_HOSTS'] != None:
  ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split()

# Application definition
DEFAULT_CONTENT_TYPE = 'text/html'

INSTALLED_APPS = (
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'tasks',
  'widget_tweaks',
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = '%s.urls' % SITE_NAME

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# Database
if os.path.join(BASE_DIR, '.db'):
  db_config_file = os.path.join(BASE_DIR, '.db')
  os.chmod(db_config_file, 0o400)
  with open(db_config_file) as f:
    s = f.read().strip()
    DATABASES = eval(s)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Tallinn'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default login pattern
LOGIN_URL = 'tasks:login'

STATIC_URL = '/static/'

STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')

# Static file path
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Sesions & security
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True
#X_FRAME_OPTIONS = 'DENY'
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_AGE = 28800 # 8 hours

# Template settings
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [str(os.path.join(BASE_DIR, 'templates'))],
    'OPTIONS': {
      'context_processors': [
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'lib.site_globals.site_title',
        'lib.site_globals.admin_site_header'
      ],
      'loaders': [
        ('django.template.loaders.cached.Loader', (
          'django.template.loaders.filesystem.Loader',
          'django.template.loaders.app_directories.Loader',
        ))
      ],
      'debug': [
        False
      ]
    },
  },
]

#from exactoris.config.prod import *
from exactoris.config import *
