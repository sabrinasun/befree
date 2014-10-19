# coding=utf-8

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.Profile'
LOGIN_REDIRECT_URL = '/account/summary'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

USERENA_WITHOUT_USERNAMES = False
USERENA_ACTIVATION_REQUIRED = True
USERENA_SIGNIN_AFTER_SIGNUP = False
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_SIGNIN_REDIRECT_URL = '/account/summary'
USERENA_USE_MESSAGES = False