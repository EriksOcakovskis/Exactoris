DEBUG = True

ALLOWED_HOSTS = ['localhost']

STATIC_URL = '/static/'

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
        True
      ]
    },
  },
]