from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from accounts.forms import UserenaSignupFormBase, SignupReaderForm
from accounts.forms import EditProfileForm
from core.views import signup as core_views_signup


from userena.views import profile_edit as userena_views_profile_edit
from userena.views import email_change as userena_views_email_change
from userena.views import password_change as userena_views_password_change
from userena.views import activate as userena_views_activate
from userena.views import email_confirm as userena_views_email_confirm



admin.autodiscover()

#urlpatterns = patterns('',
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/signup/$', core_views_signup,
            {'signup_form': UserenaSignupFormBase, "success_url": "/?msg=signup_success"},
            name='userena_signup'),
    url(r'^accounts/signup_reader/$', core_views_signup,
            {'signup_form': SignupReaderForm, "success_url": "/?msg=signup_success", "template_name": "userena/signup_reader_form.html"},
            name='userena_signup_reader'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
       userena_views_profile_edit,
       {'edit_profile_form': EditProfileForm, 'success_url':"/account/summary"},
       name='userena_profile_edit'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/from_view_bag$',
       userena_views_profile_edit,
       {'edit_profile_form': EditProfileForm, 'success_url':"/view_bag", 'extra_context':{'validate_receiver':True}},
       name='userena_profile_edit_from_view_bag'), #from view_bag for logged in accounts
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/from_inventory$',
       userena_views_profile_edit,
       {'edit_profile_form': EditProfileForm, 'success_url':"/account/material", 'extra_context':{'validate_giver': True}},
       name='userena_profile_edit_from_inventory'), #from Book I am receiving for logged in accounts

    url(r'^accounts/(?P<username>[\.\w-]+)/email/$',
       userena_views_email_change,{'success_url':"/account/summary/?msg=email_success", "template_name": "userena/email_form.html"},
       name='userena_email_change'),


    url(r'^accounts/', include('userena.urls')),
    url(r'^', include('core.urls')),
    url(r'^', include('timeline.urls')),
    url(r'^', include('network.urls')),
    # message app over contrib.umessage
    url(r'^message/', include('message.urls')),
    url(r'^message/', include('userena.contrib.umessages.urls')),

    url(r'^(?P<username>[\.\w-]+)/password/$',
       userena_views_password_change,{'success_url':"/account/summary/?msg=password_success", "template_name": "userena/password_form.html"},
       name='userena_password_change'),

    url(r'^activate/(?P<activation_key>\w+)/$', userena_views_activate, {'success_url':"/account/summary/?msg=activate_success"}, name='userena_activate' ),


    url(r'^confirm-email/(?P<confirmation_key>\w+)/$', userena_views_email_confirm, {'success_url':"/account/summary/?msg=email_change_success"}, name='userena_email_confirm'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
