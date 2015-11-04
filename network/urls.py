from django.conf.urls import patterns, url
from network.views.index_view import IndexView


urlpatterns = patterns(
    'network.views',
    url(r'^$', IndexView.as_view(), name='network_index'),
)