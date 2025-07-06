import os
from .common import *


DEBUG = False

ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = ['*']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance',
        'USER': 'postgres',
        'PASSWORD': '123456asdfgh',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}