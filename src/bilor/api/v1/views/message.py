import pprint

from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView

from bilor.core.db import connect_elasticsearch
from bilor.api.v1.throttling import MessageRateThrottle


class MessageView(APIView):
    throttle_classes = (MessageRateThrottle,)

    def get(self, request, format=None):
        return HttpResponse('get view does not do anything yet')

    def post(self, request, format=None):
        es = connect_elasticsearch()

        response = es.index(
            index=settings.ELASTICSEARCH_CONFIG['index_name'],
            doc_type='message',
            body=request.DATA)

        if response['created']:
            return HttpResponse('success')
        else:
            # TODO: Add proper erro handling
            return HttpResponse('message was not saved', code=400)
