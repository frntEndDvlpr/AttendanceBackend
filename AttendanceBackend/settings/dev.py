from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure--4lqq!qd7$=^i3#s@+x^50x1op!tg@v#l$q725d8*e6&dma=#7'

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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