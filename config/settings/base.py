# -*- coding: utf-8 -*-
"""
Django settings for Chamados CMC project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ, os

ROOT_DIR = environ.Path(__file__) - 3  # (chamados-cmc/config/settings/base.py - 3 = chamados-cmc/)
APPS_DIR = ROOT_DIR.path('chamadoscmc')

ALLOWED_HOSTS=['*']

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env.read_env(env_file=ROOT_DIR('.env'))

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
     'pipeline',
     'djangobower',
     'crispy_forms',  # Form layouts
     'compressor',
     'django_python3_ldap',
     'ldapdb',
     'autentica',
     'djcelery',
     'djcelery_email',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'chamadoscmc.core.apps.CoreConfig',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chamadoscmc.lib.error_handler.HandleBusinessExceptionMiddleware'
    
]

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
#EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='djcelery_email.backends.CeleryEmailBackend')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""DIF""", 'you@example.com'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': env('LDAP_AUTH_URL'),
     },
    'default': env.db(),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

DATABASE_ROUTERS = ['ldapdb.router.Router']


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'
#USE_TZ=True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pt-BR'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
#USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
    str(ROOT_DIR.path('components/bower_components')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.PipelineFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django_python3_ldap.auth.LDAPBackend",
    'django.contrib.auth.backends.ModelBackend',
 ]


# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

# LDAP
# ------------------------------------------------------------------------------
#LDAP_AUTH_URL = "ldap://ldap"
LDAP_AUTH_URL = env('LDAP_AUTH_URL', default='')
LDAP_AUTH_USE_TLS = env('LDAP_AUTH_USE_TLS', default=False, cast=bool)
LDAP_AUTH_SEARCH_BASE = env('LDAP_AUTH_SEARCH_BASE', default='')
LDAP_AUTH_OBJECT_CLASS = env('LDAP_AUTH_OBJECT_CLASS', default='')
LDAP_AUTH_USER_FIELDS = {
    "username": env('LDAP_AUTH_USER_FIELDS_USERNAME', default=''),
    "first_name": env('LDAP_AUTH_USER_FIELDS_FIRST_NAME', default=''),
    "last_name": env('LDAP_AUTH_USER_FIELDS_LAST_NAME', default=''),
    "email": env('LDAP_AUTH_USER_FIELDS_EMAIL', default=''),
    #"matricula": env('LDAP_AUTH_USER_FIELDS_MATRICULA', default=''),
    "pessoa": env('LDAP_AUTH_USER_FIELDS_PESSOA', default=''),
    "lotado": env('LDAP_AUTH_USER_FIELDS_LOTADO', default=''),
    "chefia": env('LDAP_AUTH_USER_FIELDS_CHEFIA', default=''),
}
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = None
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None


# LOGGING
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  
            "propagate": True,
        },
         'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# PIPELINE
# ------------------------------------------------------------------------------

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'JS_COMPRESSOR': False,
    'CSS_COMPRESSOR': False,
    'STYLESHEETS': {
        'master': {
            'source_filenames': (
              'bootstrap/dist/css/bootstrap.css',
              'jasny-bootstrap/dist/css/jasny-bootstrap.css',
              'datatables/media/css/jquery.dataTables.css',
              'datatables/media/css/dataTables.bootstrap.css',
              'login.css',
              'font-awesome/css/font-awesome.css',
              'bootstrap-select/dist/css/bootstrap-select.css',
            ),
            'output_filename': 'css/master.css',
        },
    },
    'JAVASCRIPT': {
        'master': {
            'source_filenames': (
              'jquery/dist/jquery.js',
              'bootstrap/dist/js/bootstrap.js',
              'jasny-bootstrap/dist/js/jasny-bootstrap.js',
              'underscore/underscore.js',
              'datatables/media/js/jquery.dataTables.js',
              'datatables/media/js/dataTables.bootstrap.js',
              #'vue/dist/vue.common.js',
              'vue/dist/vue.js',
              'bootstrap-select/dist/js/bootstrap-select.js',
              #'vue-strap/dist/vue-strap.js',
              #'vue-strap/dist/vue-strap-lang.js',
              'blueimp-file-upload/js/vendor/jquery.ui.widget.js',
              'blueimp-file-upload/js/jquery.iframe-transport.js',
              'blueimp-file-upload/js/jquery.fileupload.js',
            ),
            'output_filename': 'js/master.js',
        }
    }
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# BOWER
# ------------------------------------------------------------------------------

BOWER_COMPONENTS_ROOT = str(ROOT_DIR.path('components'))
BOWER_INSTALLED_APPS = (
    'jquery',
    'underscore',
    'bootstrap',
    'jasny-bootstrap',
    'datatables',
    'datatables-bootstrap3',
    'vue',
    'vue-strap',
    'fontawesome',
    'bootstrap-select',
    'jquery-file-upload',
)

# ALTERAÇÕES NO USER PARA GUARDAR INFO DO LDAP
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = 'autentica.User'

# SERVIDOR DE MICRO SERVICOS
# ------------------------------------------------------------------------------
MSCMC_SERVER = env('MSCMC_SERVER')

########## CELERY
INSTALLED_APPS += ['chamadoscmc.taskapp.celery.CeleryConfig']
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
if CELERY_BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERYD_CONCURRENCY=2
CELERYD_NODES=1
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'America/Sao Paulo'
CELERY_ENABLE_UTC = True
CELERY_DISABLE_RATE_LIMITS = True

########## END CELERY