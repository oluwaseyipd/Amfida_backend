from .base import *

DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') is not None else False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else ['yourdomain.com']

# Example production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod_db',
        'USER': 'prod_user',
        'PASSWORD': 'secret_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Enforce security protocols
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
