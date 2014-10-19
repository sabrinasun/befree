# coding=utf-8

from os.path import join

from etc import ROOT


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(ROOT, 'dev.db'),
        # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'befree',
        'USER': 'sabrina',
        'PASSWORD': 'ilucky',
        'HOST': '127.0.0.1'
    }
}
"""