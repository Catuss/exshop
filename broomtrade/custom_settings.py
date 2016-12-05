from broomtrade import settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'easy_thumbnails',
    'taggit',
    'precise_bbcode',
    'main',
    'guestbook',
    'news',
    'imagepool',
    'categories',
    'goods',
    'blog',
    'otherpage',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

STATICFILES_DIRS = [
    ('static', os.path.join(BASE_DIR, 'static')),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data/site.dat'),
    }
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'main'

SITE_ID = 1

THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_ALIASES = {
    'goods.Good.image': {
        'base': {'size': (200, 100)}
    },
}

