import environ

ROOT_DIR = environ.Path(__file__) - 3
PROJECT_DIR = ROOT_DIR.path('auction')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path('app.env')))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = env.bool('DJANGO_USE_TZ', default=True)
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='not-so-secret')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME', default=''),
        'USER': env.str('DB_USER', default=''),
        'PASSWORD': env.str('DB_PASSWORD', default=''),
        'HOST': env.str('DB_HOST', default=''),
        'PORT': env.int('DB_PORT', default=5432),
    }
}

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'auction.urls'
WSGI_APPLICATION = 'auction.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'rest_framework',
]
LOCAL_APPS = [
    'auction.core',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'


# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}


# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}


# APP SPECIFIC SETTINGS
# ------------------------------------------------------------------------------