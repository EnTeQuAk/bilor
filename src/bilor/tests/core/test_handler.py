import time
import logging

import mock

from django.conf import settings
from django.test import LiveServerTestCase
from rest_framework import status

from bilor.core.db import connect_elasticsearch
from bilor.core.handler import BilorHandler
from bilor.tests.utils.db import clear_elasticsearch_index


class TestMessageApi(LiveServerTestCase):

    def setUp(self):
        clear_elasticsearch_index()

    def tearDown(self):
        clear_elasticsearch_index()

    def _check(self, expected):
        es = connect_elasticsearch()
        es.indices.refresh()

        result = es.search(
            index=settings.ELASTICSEARCH_CONNECTION['index_name'],
            body={'query': {'match_all': {}}}
        )

        hit = result['hits']['hits'][0]
        assert hit['_type'] == 'message'
        assert hit['_source'] == expected

    def test_handler_debug(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.debug('this is a debug message')
        self._check({
            'created': mock.ANY,
            'formatted': 'this is a debug message',
            'level': logging.DEBUG,
            'logger': '_bilor_testing',
            'message': 'this is a debug message',
            'params': []
        })

    def test_handler_supports_extra_data(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.debug('this is a debug message', extra={'extra': ['foo', 'bar']})
        self._check({
            'created': mock.ANY,
            'formatted': 'this is a debug message',
            'level': logging.DEBUG,
            'logger': '_bilor_testing',
            'message': 'this is a debug message',
            'params': [],
            'extra': ['foo', 'bar']
        })

    def test_handler_warning(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

        logger.warning('this is a warning message')
        self._check({
            'created': mock.ANY,
            'formatted': 'this is a warning message',
            'level': logging.WARNING,
            'logger': '_bilor_testing',
            'message': 'this is a warning message',
            'params': [],
        })

    def test_handler_info(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        logger.info('this is an info message')
        self._check({
            'created': mock.ANY,
            'formatted': 'this is an info message',
            'level': logging.INFO,
            'logger': '_bilor_testing',
            'message': 'this is an info message',
            'params': [],
        })

    def test_handler_error(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        logger.error('this is an error message')
        self._check({
            'created': mock.ANY,
            'formatted': 'this is an error message',
            'level': logging.ERROR,
            'logger': '_bilor_testing',
            'message': 'this is an error message',
            'params': [],
        })

    def test_handler_exception(self):
        logger = logging.getLogger('_bilor_testing')
        handler = BilorHandler(self.live_server_url)
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        try:
            1 / 0
        except Exception:
            logger.exception('this is an exception message')

        es = connect_elasticsearch()
        es.indices.refresh()

        result = es.search(
            index=settings.ELASTICSEARCH_CONNECTION['index_name'],
            body={'query': {'match_all': {}}}
        )

        hit = result['hits']['hits'][0]
        assert hit['_type'] == 'message'
        source = hit['_source']

        assert source['level'] == logging.ERROR
        assert source['traceback']['title'] == 'ZeroDivisionError: division by zero'
        assert source['traceback']['exception_type'] == 'builtins.ZeroDivisionError'
