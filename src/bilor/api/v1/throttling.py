from rest_framework.throttling import AnonRateThrottle


class MessageRateThrottle(AnonRateThrottle):
    """Anonymous throttling defininition.

    This defines the scope `message` which can be easily configured
    in the settings.

    .. code:: python

        REST_FRAMEWORK = {
            'DEFAULT_THROTTLE_CLASSES': (
                'bilor.api.v1.throttling.MessageRateThrottle',
            ),
            'DEFAULT_THROTTLE_RATES': {
                'message': '60/min',
            }
        }
    """
    scope = 'message'
