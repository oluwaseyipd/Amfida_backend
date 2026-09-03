from .base import *

DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') is not None else True
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else ['localhost', '127.0.0.1']

# Use a local SQLite database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
