import os
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

# Email (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "reactdvlpr@gmail.com"
EMAIL_HOST_PASSWORD = "zubzzxvalngdulei"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Djoser Config
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}