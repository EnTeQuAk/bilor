from django.conf.urls import url, patterns


from bilor.api.v1 import views


urlpatterns = patterns(
    '',
    url(r'message/$', views.message.MessageView.as_view(), name='message')

)
