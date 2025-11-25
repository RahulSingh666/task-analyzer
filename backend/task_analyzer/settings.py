import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / 'staticfiles'


SECRET_KEY = 'replace-this-with-secure-key'
import os
DEBUG = os.environ.get("DEBUG", "False") == "True"


ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'tasks',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'task_analyzer.urls'

TEMPLATES = []

WSGI_APPLICATION = 'task_analyzer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / '../frontend'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
