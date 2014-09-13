import pprint

from django.http import HttpResponse
from django.conf import settings
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from bilor.core.db import connect_elasticsearch


class MessageView(APIView):
    #throttle_classes = (AnonRateThrottle,)

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
