from django.conf.urls import url
from .views import Home, ShareLink, ShareText, reblog, like_timelineitem, unlike_timelineitem, TimeLineItemView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^timeline/timelineitem/share_text$', login_required(ShareText.as_view()), name='text_form'),
    url(r'^timeline/timelineitem/share_link$', login_required(ShareLink.as_view()), name='link_form'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/like$', like_timelineitem, name='timelineitem_like'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/unlike$', unlike_timelineitem, name='timelineitem_unlike'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/reblog$', reblog, name='timelineitem_reblog'),
    url(r'^timeline/timelineitem/(?P<pk>\d+)/detail$', TimeLineItemView.as_view(), name='timelineitem_detail'),


]
