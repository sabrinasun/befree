# coding=utf-8

import os

from etc import ROOT


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(ROOT, 'email_files')

"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
"""
# Host for sending e-mail.
EMAIL_HOST = 'smtp.gmail.com'
# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'sabrinanyu@gmail.com'
EMAIL_HOST_PASSWORD = 'montclair'

SERVER_EMAIL = 'sabrinanyu@gmail.com'

# DEFAULT_FROM_EMAIL = 'sabrinanyu@gmail.com'
DEFAULT_FROM_EMAIL = 'support@buddhistexchange.com'