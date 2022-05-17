import json
from pathlib import Path

import environ


# Project root

BASE_DIR = Path(__file__).resolve().parent.parent


# Read environment variables

env = environ.Env(
    DEBUG=(bool, False),
)

environ.Env.read_env(BASE_DIR / '.env')


# Core settings

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

LOCAL_APPS = [
    'base_project.core',
    'base_project.rest_api',
]

THIRDPARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_hosts',
    'corsheaders',
    'storages',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRDPARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',              # django gzip
    'django_hosts.middleware.HostsRequestMiddleware',     # django-hosts
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',          # django locale
    'corsheaders.middleware.CorsMiddleware',              # django cors header
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',    # django-hosts
]

ROOT_URLCONF = 'base_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base_project.wsgi.application'


# Database

DATABASE_URL = env.get_value('DATABASE_URL', default='sqlite:///db.sqlite3')

DATABASES = {
    'default': env.db(default=DATABASE_URL),
    'readonly': env.db_url('READONLY_DATABASE_URL', default=DATABASE_URL),
}

DATABASE_ROUTERS= [
    'base_project.routers.ReadOnlyRouter'
]


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Locale

LANGUAGES = [('ja', '日本語')]

LOCALE_PATHS = [BASE_DIR / 'locale']


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = 'static/'

STATIC_URL = '/static/'


# Logging

if env('LOGGING', cast=bool, default=False):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'app': {
                'format': '%(asctime)s [%(levelname)s] %(message)s %(pathname)s:%(lineno)d',
                'datefmt' : '%Y/%m/%d %H:%M:%S',
            },
            'db': {
                'format': '%(message)s',
            },
        },
        'filters': {
            'query_filter': {
                '()': 'base_project.logging.QueryFilter',
            }
        },
        'handlers': {
            'app': {
                'level': 'INFO',
                'formatter': 'app',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR / 'logs/app.log',
                'maxBytes': 500000,
                'backupCount': 5,
            },
            'db': {
                'level': 'DEBUG',
                'formatter': 'db',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR / 'logs/db.log',
                'maxBytes': 500000,
                'backupCount': 5,
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['db'],
                'propagate': False,
                'filters': ['query_filter']
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['app'],
        },
    }


# django-hosts

DEFAULT_HOST = 'admin'

ROOT_HOSTCONF = 'base_project.hosts'


# Django CORS headers

CORS_ALLOW_ALL_ORIGINS = DEBUG

CORS_ALLOWED_ORIGINS = []


# CSRF

CSRF_TRUSTED_ORIGINS = [
    'https://*.127.0.0.1',
]


# Amazon Cognito

AMAZON_COGNITO_REGION =  env('AMAZON_COGNITO_REGION')

AMAZON_COGNITO_NETLOC = f'cognito-idp.{AMAZON_COGNITO_REGION}.amazonaws.com'

AMAZON_COGNITO_POOL_ID = env('AMAZON_COGNITO_POOL_ID')

AMAZON_COGNITO_ISSUER = f'https://{AMAZON_COGNITO_NETLOC}/{AMAZON_COGNITO_POOL_ID}'

AMAZON_COGNITO_CLIENT_ID = env('AMAZON_COGNITO_CLIENT_ID')

with open(BASE_DIR / 'jwks.json', 'r', encoding='utf-8') as f:
    AMAZON_COGNITO_JWKS = json.load(f)


# Django rest framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    # ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/minute',
        'user': '200/minute',
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomCursorPagination',
    # 'PAGE_SIZE': 10,
    # 'EXCEPTION_HANDLER': 'api.exceptions.exception_handler',

}


# AWS CloudFront

AWS_CLOUDFRONT_DOMAIN = env('AWS_CLOUDFRONT_DOMAIN')


# AWS S3

AWS_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')

AWS_S3_REGION_NAME =  env('AWS_S3_REGION')

AWS_STORAGE_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')

AWS_S3_OBJECT_PARAMETERS = { 'CacheControl': 'max-age=86400' }

AWS_DEFAULT_ACL = 'public-read'


# media files

MEDIA_ROOT = str(BASE_DIR / 'media') + '/'

MEDIA_URL = '/media/'


if AWS_CLOUDFRONT_DOMAIN:

    DEFAULT_FILE_STORAGE = 'base_project.backends.MediaStorage'

    MEDIA_URL = f'//{AWS_CLOUDFRONT_DOMAIN}/media/'
