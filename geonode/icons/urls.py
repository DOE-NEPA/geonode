from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import IconDetailView

urlpatterns = patterns('geonode.icons.views',
                       url(r'^$',
                           TemplateView.as_view(template_name='icons/icon_list.html'),
                           name="icon_list"),
                       url(r'^create/$',
                           'icon_create',
                           name="icon_create"),
                       url(r'^icon/(?P<slug>[-\w]+)/$',
                           IconDetailView.as_view(),
                           name='icon_detail'),
                       url(r'^icon/(?P<slug>[-\w]+)/update/$',
                           'icon_update',
                           name='icon_update'),
                       url(r'^icon/(?P<slug>[-\w]+)/remove/$',
                           'icon_remove',
                           name='icon_remove'),
                       )
