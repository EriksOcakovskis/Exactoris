"""
Django settings for hd2wo project.

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

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split()


# Application definition

INSTALLED_APPS = (
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'workorders',
  'smart_selects',
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
)

ROOT_URLCONF = '%s.urls' % SITE_NAME

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
  'lib.site_globals.site_title',
  'lib.site_globals.admin_site_header',
)

# Database
db_config_file = os.path.join(BASE_DIR, '.db')
os.chmod(db_config_file, 0o400)
with open(db_config_file) as f:
  s = f.read().strip()
  DATABASES = eval(s)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Tallinn'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default login pattern
LOGIN_URL = 'workorders:login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')

# Static file path
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Template directory path
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Sesions
SESSION_COOKIE_AGE = 28800 # 8 hours
