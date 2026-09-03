import os
from split_settings.tools import include

# Default to development if DJANGO_ENV is not explicitly set
ENV = os.environ.get('DJANGO_ENV', 'development')

base_settings = [
    'base.py',
    f'{ENV}.py',
]

include(*base_settings)