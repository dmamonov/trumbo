"""Base settings to build other settings files upon."""
import os
from datetime import timedelta

import environ

APP_NAME = 'screenplaywritter'

API_URI = 'api/v1'

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('api')

env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)

# Language and timezone
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-en'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST')
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = False

# URLs
ROOT_URLCONF = 'config.urls'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# ASGI
ASGI_APPLICATION = 'config.asgi.application'

# Users & Authentication
AUTH_USER_MODEL = 'users.User'

# Apps
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "admin_interface",
    "colorfield",
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'modeltranslation',
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_rest_passwordreset',
    'corsheaders',
    'django_filters',
    'ckeditor',
    'ckeditor_uploader'
]

LOCAL_APPS = [
    'api.users.apps.UsersAppConfig',
    'api.authentication.apps.AuthenticationAppConfig',
    'api.cms.apps.CMSAppConfig',
    'api.events.apps.EventsAppConfig',
    'api.screenplays.apps.ScreenPlayAppConfig',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

# only if django version >= 3.0
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Passwords
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

# Static files
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
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

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

# Admin
ADMIN_URL = 'admin/'
CUSTOMER_ADMIN_URL = 'customer/'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "api.utils.auth0.validator.DoubleAuthentication",
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12,
}

# AUTOFIELD
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MAIN_DATE_FORMAT = "%Y-%m-%d"
MAIN_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# CMS


def gettext(s): return s


LANGUAGES = (
    ('es', gettext('Spanish')),
    ('en', gettext('English')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

# MODELTRANSLATION_TRANSLATION_FILES = (
#    'cms.translation',
# )
MODELTRANSLATION_AUTO_POPULATE = True

# Authentication

SIMPLE_JWT = {
    # Cookie name. Enables cookies if value is set.
    'ACCESS_TOKEN_COOKIE': 'ACCESS',
    # Whether the auth cookies should be secure (https:// only).
    'ACCESS_TOKEN_COOKIE_SECURE': True,
    # Http only cookie flag.It's not fetch by javascript.
    'ACCESS_TOKEN_COOKIE_HTTP_ONLY': True,
    # Whether to set the flag restricting cookie leaks on cross-site requests.
    'ACCESS_TOKEN_COOKIE_SAMESITE': 'Lax',
    # Cookie name. Enables cookies if value is set.
    'REFRESH_TOKEN_COOKIE': 'REFRESH',
    # Whether the auth cookies should be secure (https:// only).
    'REFRESH_TOKEN_COOKIE_SECURE': True,
    # Http only cookie flag.It's not fetch by javascript.
    'REFRESH_TOKEN_COOKIE_HTTP_ONLY': True,
    # Whether to set the flag restricting cookie leaks on cross-site requests.
    'REFRESH_TOKEN_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_DOMAIN': "{{app_name}}",
}
# external token format
AUTHENTICATION_EXTERNAL_MESSAGE_PROVIDERS = [
    {'name': 'console', "has_title": False},
    {'name': 'sms', "has_title": False},
    {'name': 'email', "has_title": True}
]
AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_DEFAULT = os.getenv(
    'AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_CONSOLE', 'This is your token for {app_name}: {token}')
AUTHENTICATION_EXTERNAL_TOKEN_MESSAGE_FORMATS = {
    provider["name"]: {
        'validate_account': os.getenv(f'AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_{provider["name"].upper()}_VALIDATE_ACCOUNT', AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_DEFAULT),
        'recover_account': os.getenv(f'AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_{provider["name"].upper()}_RECOVER_ACCOUNT', AUTHENTICATION_EXTERNAL_MESSAGE_FORMAT_DEFAULT),
    } for provider in AUTHENTICATION_EXTERNAL_MESSAGE_PROVIDERS
}

AUTHENTICATION_EXTERNAL_TITLE_FORMAT_DEFAULT = os.getenv(
    'AUTHENTICATION_EXTERNAL_TITLE_FORMAT_CONSOLE', '{app_name} {message_type}')

AUTHENTICATION_EXTERNAL_TOKEN_TITLE_FORMATS = {
    provider["name"]: {
        'validate_account': os.getenv(f'AUTHENTICATION_EXTERNAL_TITLE_FORMAT_{provider["name"].upper()}_VALIDATE_ACCOUNT', AUTHENTICATION_EXTERNAL_TITLE_FORMAT_DEFAULT),
        'recover_account': os.getenv(f'AUTHENTICATION_EXTERNAL_TITLE_FORMAT_{provider["name"].upper()}_RECOVER_ACCOUNT', AUTHENTICATION_EXTERNAL_TITLE_FORMAT_DEFAULT),
    } for provider in AUTHENTICATION_EXTERNAL_MESSAGE_PROVIDERS if provider['has_title']
}

# external token times
AUTHENTICATION_EXTERNAL_TOKEN_RESEND = {
    'validate_account': timedelta(seconds=int(os.getenv(f'AUTHENTICATION_EXTERNAL_TOKEN_RESEND_VALIDATE_ACCOUNT_SECONDS', '60'))),
    'recover_account': timedelta(seconds=int(os.getenv(f'AUTHENTICATION_EXTERNAL_TOKEN_RESEND_RECOVER_ACCOUNT_SECONDS', '60'))),
}

AUTHENTICATION_EXTERNAL_TOKEN_EXPIRY = {
    'validate_account': timedelta(hours=int(os.getenv(f'AUTHENTICATION_EXTERNAL_TOKEN_EXPIRY_VALIDATE_ACCOUNT_HOURS', '5'))),
    'recover_account': timedelta(hours=int(os.getenv(f'AUTHENTICATION_EXTERNAL_TOKEN_EXPIRY_RECOVER_ACCOUNT_HOURS', '5'))),
}


# Auth0 Authentication
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('API_IDENTIFIER')

DRF_PYJWT_KWARGS = {"audience": os.getenv('AUTH0_CLIENT_ID')}
DRF_PYJWT_LOOKUP_USER = 'api.utils.auth0.user.lookup_user.lookup_user'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_PHONE_NUMBER = os.getenv('TWILIO_FROM_PHONE_NUMBER')

# Styles
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'toolbar': 'full',
        # other CKEditor config options here
    },
}