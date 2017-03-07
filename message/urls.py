from django.conf.urls import url
from .views import UserMessageDetailListView, send_message, BoardMessageCreateView,BoardMessageListView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^view/(?P<username>[\.\w]+)/$', login_required(UserMessageDetailListView.as_view()), name='user_message_list_detail'),
    url(r'^compose/$', send_message, name='userena_umessages_compose'),
    url(r'^board/(?P<pk>\d+)/$', login_required(BoardMessageListView.as_view()), name='boardmessage_list'),
    url(r'^board/(?P<pk>\d+)/new$', login_required(BoardMessageCreateView.as_view()), name='boardmessage_new'),

]
