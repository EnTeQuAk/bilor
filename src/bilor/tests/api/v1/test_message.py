from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from bilor.tests.utils.db import clear_elasticsearch_index
from bilor.core.db import connect_elasticsearch


class TestMessageApi(APITestCase):

    def setUp(self):
        clear_elasticsearch_index()

    def tearDown(self):
        clear_elasticsearch_index()

    def test_create_new_message(self):
        url = reverse('api-v1:message')

        # We do not yet actually validate the data. So check that
        # we simply save it in elastic search.
        data = {'test': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, b'success')

        es = connect_elasticsearch()
        es.indices.refresh()

        result = es.search(
            index=settings.ELASTICSEARCH_CONNECTION['index_name'],
            body={'query': {'match_all': {}}}
        )

        hit = result['hits']['hits'][0]
        assert hit['_type'] == 'message'
        assert hit['_source'] == {'test': 'test'}
