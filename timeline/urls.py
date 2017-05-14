from django.conf.urls import url
from .views import Home, ShareLink, ShareText, reblog, like_timelineitem, unlike_timelineitem,\
    TimeLineItemView, TimeLineItemComment, ShareTextUpdateView, ShareLinkUpdateView,\
    retrieve_titles, retrieve_topics, retrieve_teachers
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^timeline/(?P<category_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/$', Home.as_view(), name='item_list'),
    url(r'^timeline/(?P<category_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/(?P<post_slug>[-\w]+)/$', TimeLineItemView.as_view(), name='timelineitem_detail'),
    url(r'^timeline/timelineitem/share_text$', login_required(ShareText.as_view()), name='text_form'),
    url(r'^timeline/timelineitem/share_link$', login_required(ShareLink.as_view()), name='link_form'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/like$', like_timelineitem, name='timelineitem_like'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/unlike$', unlike_timelineitem, name='timelineitem_unlike'),
    url(r'^timeline/timelineitem/(?P<timelineitem_id>\d+)/reblog$', reblog, name='timelineitem_reblog'),
    #url(r'^timeline/timelineitem/(?P<pk>\d+)/detail$', TimeLineItemView.as_view(), name='timelineitem_detail'),
    url(r'^timeline/timelineitem/(?P<pk>\d+)/comment$', TimeLineItemComment.as_view(), name='timelineitem_comment'),
    url(r'^timeline/timelineitem/(?P<pk>\d+)/edit/sharetext$', ShareTextUpdateView.as_view(), name='timelineitem_edit_text'),
    url(r'^timeline/timelineitem/(?P<pk>\d+)/edit/sharelink$', ShareLinkUpdateView.as_view(), name='timelineitem_edit_link'),
    url(r'^timeline/timelineitem/titles$', retrieve_titles, name='timelineitem_titles'),
    url(r'^timeline/timelineitem/teachers$', retrieve_teachers, name='timelineitem_teachers'),
    url(r'^timeline/timelineitem/topics$', retrieve_topics, name='timelineitem_topics'),

]
