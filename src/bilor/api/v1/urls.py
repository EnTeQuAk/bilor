from django.conf.urls import url, patterns


from bilor.api.v1 import views as v1_views


urlpatterns = patterns(
    '',
    url(r'message/$', v1_views.message.MessageView.as_view())

)
