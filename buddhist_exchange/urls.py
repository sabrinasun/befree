from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from accounts.forms import SignupForm, SignupReaderForm
from accounts.forms import EditProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/signup/$', 'core.views.signup', 
            {'signup_form': SignupForm, "success_url": "/?msg=signup_success"},
            name='userena_signup'),
    url(r'^accounts/signup_reader/$', 'core.views.signup', 
            {'signup_form': SignupReaderForm, "success_url": "/?msg=singup_success", "template_name": "userena/signup_reader_form.html"},
            name='userena_signup_reader'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
       'userena.views.profile_edit',
       {'edit_profile_form': EditProfileForm, 'success_url':"/account/summary"},
       name='userena_profile_edit'),

    url(r'^accounts/(?P<username>[\.\w-]+)/email/$',
       'userena.views.email_change',{'success_url':"/account/summary/?msg=email_success", "template_name": "userena/email_form.html"},
       name='userena_email_change'),                       

      
    url(r'^accounts/', include('userena.urls')),
    url(r'^', include('core.urls')),
    
    url(r'^(?P<username>[\.\w-]+)/password/$',
       'userena.views.password_change',{'success_url':"/account/summary/?msg=password_success", "template_name": "userena/password_form.html"},
       name='userena_password_change'),    
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
