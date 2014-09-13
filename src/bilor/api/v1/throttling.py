from rest_framework.throttling import AnonRateThrottle


class MessageRateThrottle(AnonRateThrottle):
    scope = 'message'
