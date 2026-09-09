"""Production settings for Render, Supabase, Cloudflare R2, and Resend."""

import os

import dj_database_url
from .base import *


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in {
        '1', 'true', 'yes', 'on'
    }


def env_list(name, default=''):
    return [value.strip() for value in os.getenv(name, default).split(',') if value.strip()]


DEBUG = env_bool('DEBUG', False)
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS', 'https://amfida.vercel.app')

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DB_URL'],
        conn_max_age=600,
        ssl_require=True,
    )
}

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS', 'https://amfida.vercel.app')
CORS_ALLOW_CREDENTIALS = False

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

EMAIL_BACKEND = 'anymail.backends.resend.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
ANYMAIL = {
    'RESEND_API_KEY': os.environ['RESEND_API_KEY'],
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

USE_S3 = env_bool('USE_S3', True)
if USE_S3:
    INSTALLED_APPS.append('storages')

    AWS_ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['STORAGE_BUCKET_NAME']
    AWS_S3_ENDPOINT_URL = os.environ['S3_ENDPOINT_URL']
    AWS_S3_REGION_NAME = os.getenv('S3_REGION_NAME', 'auto')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('S3_CUSTOM_DOMAIN', '').rstrip('/')
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False

    STORAGES['default'] = {
        'BACKEND': 'storages.backends.s3.S3Storage',
    }
    MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN}/' if AWS_S3_CUSTOM_DOMAIN else (
        f'{AWS_S3_ENDPOINT_URL.rstrip("/")}/{AWS_STORAGE_BUCKET_NAME}/'
    )
else:
    STORAGES['default'] = {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    }
    MEDIA_URL = '/media/'
