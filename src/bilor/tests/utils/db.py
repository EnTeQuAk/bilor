import elasticsearch

from django.conf import settings

from bilor.core.db import connect_elasticsearch


def clear_elasticsearch_index():
    es = connect_elasticsearch()
    es.indices.delete(index=settings.ELASTICSEARCH_CONNECTION['index_name'])
    es.indices.refresh()
