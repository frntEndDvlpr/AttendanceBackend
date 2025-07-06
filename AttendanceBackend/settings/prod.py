import os
import dj_database_url
from .common import *


DEBUG = False

ALLOWED_HOSTS = ['attendance-ksa-247f689c4e51.herokuapp.com']
CORS_ALLOWED_ORIGINS = ['*']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': dj_database_url.config()
}