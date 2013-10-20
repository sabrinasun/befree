from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from accounts.forms import SignupForm, SignupReaderForm
from accounts.forms import EditProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/signup/$', 'userena.views.signup', 
            {'signup_form': SignupForm, "success_url": "/?msg=signup"},
            name='userena_signup'),
    url(r'^accounts/signup_reader/$', 'userena.views.signup', 
            {'signup_form': SignupReaderForm, "success_url": "/check_out/", "template_name": "userena/signup_reader_form.html"},
            name='userena_signup_reader'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
       'userena.views.profile_edit',
       {'edit_profile_form': EditProfileForm},
       name='userena_profile_edit'),

    url(r'^accounts/', include('userena.urls')),
    url(r'^', include('core.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
