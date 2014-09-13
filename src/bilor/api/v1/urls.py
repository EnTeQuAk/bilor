from django.conf.urls import url, patterns


from bilor.api.v1 import message


urlpatterns = patterns(
    '',
    url(r'message/$', message.MessageView.as_view())

)
