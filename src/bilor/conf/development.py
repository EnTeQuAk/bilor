from bilor.conf.base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

ELASTICSEARCH_CONNECTION = {
    'hosts': ['localhost'],
    'index_name': 'bilor_dev',
    'sniff_on_start': True,
    'sniff_on_connection_fail': True,
    'sniffer_timeout': 60
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOGGING['loggers']['root']['level'] = 'DEBUG'
LOGGING['loggers']['celery']['level'] = 'DEBUG'
LOGGING['loggers']['bilor']['level'] = 'DEBUG'
