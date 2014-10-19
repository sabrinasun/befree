# coding=utf-8

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin'

)

# user defined apps
INSTALLED_APPS += (
    'south',
    'userena',
    'guardian',
    'easy_thumbnails',
    'endless_pagination',
    'accounts',
    'core',
)