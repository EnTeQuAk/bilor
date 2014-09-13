from django.conf import settings
import os
import os.path


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'bilor.conf.test'

    settings.DATABASES['default'].update({
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    })

    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'bilor.tests',
    )
