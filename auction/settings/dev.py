from .base import *  # noqa

ROOT_URLCONF = "auction.dev_urls"

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
INSTALLED_APPS += ['debug_toolbar']  # noqa F405
INTERNAL_IPS = ['127.0.0.1']

# whitenoise
# ------------------------------------------------------------------------------
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')  # noqa F405
