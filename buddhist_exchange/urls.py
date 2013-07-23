from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from accounts.forms import SignupForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/signup/$', 'userena.views.signup', 
            {'signup_form': SignupForm},
            name='userena_signup'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^', include('core.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
