"""Production settings."""

from .base import *  # NOQA
from .base import env
from datetime import timedelta
import os
import json

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from corsheaders.defaults import default_headers

# AWS Patameters
AWS_REGION = os.getenv('AWS_REGION', 'us-east-2')

# set django variables
DEBUG = os.getenv('DJANGO_DEBUG') == 'True'

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', None)

# Base
SECRET_KEY = '$!*vq%gk*aj^624m)koo#myp5tdlx%hlk%)&1p9tca-10*mas-'
ALLOWED_HOSTS = ['*']

# Databases
DB_CREDENTIALS = os.getenv('DB_CREDENTIALS')
if DB_CREDENTIALS:
    DB_CREDENTIALS = json.loads(DB_CREDENTIALS)
    DATABASE_DEFAULT = {
        'ENGINE': DB_CREDENTIALS.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': DB_CREDENTIALS.get('DB_DATABASE'),
        'USER': DB_CREDENTIALS.get('DB_USER'),
        'PASSWORD': DB_CREDENTIALS.get('DB_PASSWORD'),
        'PORT': DB_CREDENTIALS.get('DB_PORT'),
        'HOST': DB_CREDENTIALS.get('DB_HOST'),
    }
else:
    DATABASE_DEFAULT = {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_DATABASE'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT'),
        'HOST': os.getenv('DB_HOST'),
    }

DATABASES = {
    'default': DATABASE_DEFAULT
}
DATABASES['default']['ATOMIC_REQUESTS'] = False
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA

if DATABASES['default']['ENGINE'] == 'postgres':
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# Admin
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin')

# Middleware
MIDDLEWARE += []

# Gunicorn
INSTALLED_APPS = ['daphne'] + INSTALLED_APPS  # noqa F405
INSTALLED_APPS += ['storages']  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405


# Logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            "hosts": [(os.getenv('REDIS_CHANNEL_LAYER_HOST'), 6379)],
        },
    },
}

# Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN and ENVIRONMENT == 'PRODUCTION':
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Media
# aws settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME =  os.getenv('AWS_STORAGE_BUCKET_NAME', None)
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-2')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True

AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
if os.getenv('CORS_ALLOWED_ORIGINS', None) != '*':
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
    print('CORS_ALLOWED_ORIGINS', CORS_ALLOWED_ORIGINS)
else:
    CORS_ALLOW_ALL_ORIGINS = True
print('CORS_ALLOW_ALL_ORIGINS', CORS_ALLOW_ALL_ORIGINS)
print('CORS_ALLOW_CREDENTIALS', CORS_ALLOW_CREDENTIALS)

CORS_ALLOW_HEADERS = list(default_headers) + [
    SIMPLE_JWT['ACCESS_TOKEN_COOKIE'].lower(),
    SIMPLE_JWT['REFRESH_TOKEN_COOKIE'].lower(),
]

# Email
EMAIL_NO_REPLY = os.getenv('EMAIL_NO_REPLY', 'noreply@mail.com')
