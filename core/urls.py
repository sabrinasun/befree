from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import GiverMaterialCreateView, GiverMaterialEditView


def to_template(template_name):
    return TemplateView.as_view(template_name=template_name)

urlpatterns = patterns('core.views',
    url(r'^$', 'index', name='index'),
    url(r'^to-giver/$', to_template('to-giver.html'), name='to_giver'),
    url(r'^to-reader/$', to_template('to-reader.html'), name='to_reader'),
    url(r'^shipping/$', to_template('shipping.html'), name='shipping'),
    url(r'^help/$', to_template('help.html'), name='help'),
    url(r'^account/summary/$', 'account_summary', name='account_summary'),
    url(r'^account/orders/reading/$', 'account_reading_orders', name='account_reading_orders'),
    url(r'^account/orders/giving/$', 'account_giving_orders', name='account_giving_orders'),
    url(r'^account/material/$', 'account_material', name='account_material'),
    url(r'^account/material/new/$', 'account_material_edit', name='account_material_new'),
    url(r'^account/giver-material/new/$', login_required(GiverMaterialCreateView.as_view()),
        name='giver_material_new'),
    url(r'^account/givermatrial/edit/(?P<pk>\d+)/$', login_required(GiverMaterialEditView.as_view()),
        name='giver_material_edit'),
    url(r'^account/material/(?P<material_id>\d+)/edit/$', 'account_material_edit', name='account_material_edit'),
    url(r'^account/add/publisher/$', 'account_add_publisher', name='account_add_publisher'),
    
    url(r'^account/material/new/existing/$', to_template('account/material_new_from_existing.html'),
        name='material_new_from_existing'),
    url(r'^add/(?P<model_name>\w+)/?$', 'add_new_model', name="add_new_model"),
    url(r'^users/(?P<username>[\w.@+-]+)/$', 'user_profile', name='user_profile'),
    url(r'^check_out/$', 'check_out', name='check_out'),
    url(r'^order/(?P<order_id>\d+)/ship/$', 'ship_order', name='ship_order'),
)
