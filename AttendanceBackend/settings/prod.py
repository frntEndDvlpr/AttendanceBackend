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
    'default': dj_database_url.config()
}