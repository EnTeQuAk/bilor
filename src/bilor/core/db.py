#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from django.conf import settings


def connect_elasticsearch():
    """Connect to ElasticSearch and ensure our base index exists."""
    config = settings.ELASTICSEARCH_CONNECTION.copy()

    # TODO: Add support for multiple indices.

    index_name = config.pop('index_name')

    es = Elasticsearch(**config)
    if not es.indices.exists(index_name):
        es.indices.create(index_name)
    return es
