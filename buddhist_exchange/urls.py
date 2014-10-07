from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from accounts.forms import UserenaSignupFormBase, SignupReaderForm
from accounts.forms import EditProfileForm


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/signup/$', 'core.views.signup',
                           {'signup_form': UserenaSignupFormBase,
                            "success_url": "/?msg=signup_success"},
                           name='userena_signup'),
                       url(r'^accounts/signup_reader/$', 'core.views.signup',
                           {'signup_form': SignupReaderForm,
                            "success_url": "/?msg=signup_success",
                            "template_name":
                                "userena/signup_reader_form.html"},
                           name='userena_signup_reader'),
                       url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
                           'userena.views.profile_edit',
                           {'edit_profile_form': EditProfileForm,
                            'success_url': "/account/summary"},
                           name='userena_profile_edit'),
                       url(
                           r'^accounts/(?P<username>['
                           r'\.\w-]+)/edit/from_view_bag$',
                           'userena.views.profile_edit',
                           {'edit_profile_form': EditProfileForm,
                            'success_url': "/view_bag",
                            'extra_context': {'validate_receiver': True}},
                           name='userena_profile_edit_from_view_bag'),
                       # from view_bag for logged in accounts

                       url(
                           r'^accounts/(?P<username>['
                           r'\.\w-]+)/edit/from_inventory$',
                           'userena.views.profile_edit',
                           {'edit_profile_form': EditProfileForm,
                            'success_url': "/account/material",
                            'extra_context': {'validate_giver': True}},
                           name='userena_profile_edit_from_inventory'),
                       #from Book I am receiving for logged in accounts


                       url(r'^accounts/(?P<username>[\.\w-]+)/email/$',
                           'userena.views.email_change', {
                           'success_url':
                               "/account/summary/?msg=email_success",
                           "template_name": "userena/email_form.html"},
                           name='userena_email_change'),


                       url(r'^accounts/', include('userena.urls')),
                       url(r'^', include('core.urls')),

                       url(r'^(?P<username>[\.\w-]+)/password/$',
                           'userena.views.password_change', {
                           'success_url': "/account/summary/?msg=password_success",
                           "template_name": "userena/password_form.html"},
                           name='userena_password_change'),

                       url(r'^activate/(?P<activation_key>\w+)/$',
                           'userena.views.activate', {
                           'success_url': "/account/summary/?msg=activate_success"},
                           name='userena_activate'),


                       url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
                           'userena.views.email_confirm', {
                           'success_url': "/account/summary/?msg=email_change_success"},
                           name='userena_email_confirm'),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
