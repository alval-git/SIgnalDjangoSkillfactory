import django_heroku
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'please-set-secret-key-through-env')

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks.apps.TasksConfig',
]

ROOT_URLCONF = 'todoapp.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'todoapp.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'ru-RU'


django_heroku.settings(locals())


def get_cache():
    environment_ready = all(
        os.environ.get(f'MEMCACHIER_{key}', False)
        for key in ['SERVERS', 'USERNAME', 'PASSWORD']
    )
    if not environment_ready:
        cache = {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
    else:
        servers = os.environ['MEMCACHIER_SERVERS']
        username = os.environ['MEMCACHIER_USERNAME']
        password = os.environ['MEMCACHIER_PASSWORD']
        cache = {
            'default': {
                'BACKEND': 'django_bmemcached.memcached.BMemcached',
                'TIMEOUT': None,
                'LOCATION': servers,
                'OPTIONS': {
                    'username': username,
                    'password': password,
                }
            }
        }
    return {'default': cache}


CACHES = get_cache()

# CACHES = { 
#     'default': {
#         'BACKEND':  'django.core.cache.backends.memcached.MemcachedCache', 
#         'LOCATION': '127.0.0.1:11211', 
#         }
# }