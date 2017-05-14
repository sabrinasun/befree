from django.conf.urls import url
from .views import UserPublicPage, follow_user, unfollow_user

urlpatterns = [
    url(r'^network/user/(?P<pk>\d+)/$', UserPublicPage.as_view(), name='user_public'),
    url(r'^network/user/(?P<pk>\d+)/(?P<category_slug>\w+)/(?P<topic_slug>\w+)/$', UserPublicPage.as_view(), name='user_public_list'),
    url(r'^network/user/(?P<unfollow_user_id>\d+)/unfollow$', unfollow_user, name='user_unfollow'),
    url(r'^network/user/(?P<follow_user_id>\d+)/follow$', follow_user, name='user_follow'),
]
