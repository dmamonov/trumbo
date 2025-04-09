"""Development settings."""

from datetime import timedelta

from .base import *  # NOQA
from .base import env

print("CHK SETTINGS 1")
# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "*"
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA


# Middleware
MIDDLEWARE += []

# django-extensions
INSTALLED_APPS += ['django_extensions', 'drf_yasg', ]  # , 'drf_yasg'# noqa F405

# Simple JWT

SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
})

# Channels (Web Socket)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://default@127.0.0.1:6379')],
        },
    },
}

# Front end URL
FRONT_END_URL = os.environ.get('FRONT_END_URL', 'http://localhost:3000')

# Media
PUBLIC_MEDIA_LOCATION = 'media'

# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
    'http://localhost:3002',
)

# Environment
ENVIRONMENT = os.environ.get('ENVIRONMENT', None)

# Email
EMAIL_NO_REPLY = os.environ.get('EMAIL_NO_REPLY', 'noreply@mail.com')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 8025
