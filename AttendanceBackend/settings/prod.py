import os
import dj_database_url
from .common import *


DEBUG = False

CORS_ALLOW_ALL_ORIGINS = False
ALLOWED_HOSTS = ['attendance-ksa-247f689c4e51.herokuapp.com']
CORS_ALLOWED_ORIGINS = [
    'https://attendance-ksa-247f689c4e51.herokuapp.com',
    'http://64.23.176.226:8069/web#action=714&model=attendance.api.config&view_type=list&cids=1&menu_id=429',
]

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Email (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Djoser Config
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}