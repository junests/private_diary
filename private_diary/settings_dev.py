from .settings_common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Logging
Logging = {
    'version': 1,
    'disable_existing_loggers': False,

    # logger
    'loggers': {
        # django
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # app
        'diary': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
    # handler
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },
    # formatter
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
