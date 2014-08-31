from django.contrib import admin
from django.conf.urls import url, include, patterns

from bilor.web import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='bilor-index'),

    # Hookup our REST Api
    url(r'^api/v1/', include('bilor.api.v1.urls', namespace='api-v1')),
)
