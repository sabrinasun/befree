from django.conf.urls import url
from .views import Home, ShareLink, ShareText
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^timeline/timelineitem/share_text$', login_required(ShareText.as_view()), name='text_form'),
    url(r'^timeline/timelineitem/share_link$', login_required(ShareLink.as_view()), name='link_form'),

]
