from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status

from bilor.core.db import connect_elasticsearch
from bilor.api.v1.throttling import MessageRateThrottle


class MessageView(APIView):
    """Simple api view that stores messages.

    Messages technically can contain any possible
    json-serializable data.

    For now there is no verification, yet this would
    be a great idea to not allow spam to come forword.
    """
    throttle_classes = (MessageRateThrottle,)

    def get(self, request, format=None):
        return HttpResponse('get view does not do anything yet')

    def post(self, request, format=None):
        es = connect_elasticsearch()

        response = es.index(
            index=settings.ELASTICSEARCH_CONNECTION['index_name'],
            doc_type='message',
            body=request.DATA)

        if response['created']:
            return HttpResponse('success', status=status.HTTP_201_CREATED)
        else:
            # TODO: Add proper error handling
            return HttpResponse(
                'message was not saved',
                status=status.HTTP_400_BAD_REQUEST)
