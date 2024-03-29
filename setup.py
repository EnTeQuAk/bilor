#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('README.rst') as fobj:
    readme = fobj.read()

with open('CHANGELOG.rst') as fobj:
    history = fobj.read()
    history.replace('.. :changelog:', '')


test_requires = [
    # General test libraries
    'tox>=1.7.1,<1.8',
    'py>=1.4.20,<1.5',
    'pytest>=2.5.2,<2.6',
    'pytest-django>=2.6.1,<2.7',

    # Pep8 and code quality checkers
    'pyflakes>=0.8.1,<0.9',
    'coverage>=3.7.1,<3.8',
    'pytest-cov>=1.6,<1.7',
    'pytest-flakes>=0.2,<1.0',
    'pytest-pep8>=1.0.5,<1.1',
    'pep8>=1.4.6,<1.5',
    'coverage>=3.7.1,<3.8',

    # Fixtures, test helpers
    'factory-boy>=2.3.1,<2.4',
    'mock>=1.0.1,<1.1',
    'httpretty>=0.8.0',
]


install_requires = [
    # General dependencies
    'django>=1.7,<1.8',

    # For async worker support
    'celery>=3.1,<3.2',
    'django-celery>=3.1,<3.2',

    # For our REST Api
    'djangorestframework>=2.3.14,<2.4',

    # Our data storage backend
    'elasticsearch',
    'elasticsearch-dsl',

    # Traceback extraction tools.
    'werkzeug',

    # For the example client.
    'requests',
]


docs_requires = [
    'sphinx',
    'sphinx_rtd_theme'
]


class PyTest(TestCommand):
    user_options = [
        ('cov=', None, 'Run coverage'),
        ('cov-xml=', None, 'Generate junit xml report'),
        ('cov-html=', None, 'Generate junit html report'),
        ('junitxml=', None, 'Generate xml of test results'),
        ('clearcache', None, 'Clear cache first')
    ]
    boolean_options = ['clearcache']

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.cov_xml = False
        self.cov_html = False
        self.junitxml = None
        self.clearcache = False

    def run_tests(self):
        import pytest

        params = {'args': self.test_args}

        if self.cov is not None:
            params['plugins'] = ['cov']
            params['args'].extend(
                ['--cov', self.cov, '--cov-report', 'term-missing'])
            if self.cov_xml:
                params['args'].extend(['--cov-report', 'xml'])
            if self.cov_html:
                params['args'].extend(['--cov-report', 'html'])
        if self.junitxml is not None:
            params['args'].extend(['--junitxml', self.junitxml])
        if self.clearcache:
            params['args'].extend(['--clearcache'])

        self.test_suite = True

        errno = pytest.main(**params)
        sys.exit(errno)

setup(
    name='bilor',
    version='0.1.0',
    description='Experimental exception/logging server.',
    long_description=readme + '\n\n' + history,
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='https://github.com/EnTEQuAk/bilor/',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    test_suite='src',
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    extras_require={
        'docs': docs_requires,
        'tests': test_requires,
    },
    zip_safe=False,
    license='BSD',
    classifiers=[
        '__DO NOT UPLOAD__',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
