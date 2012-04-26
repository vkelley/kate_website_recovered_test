from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from userena import views as userena_views

from accounts.forms import EditFormExtra
from tick.api import *
from mobile_apps.api import AppResource, TypeResource

from userena import views as userena_views

from accounts.forms import EditFormExtra

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(CommonCoreResource())
v1_api.register(ContentAreaResource())
v1_api.register(LevelResource())
v1_api.register(ResourceResource())
v1_api.register(TechnologyStandardResource())
v1_api.register(AppResource())
v1_api.register(TypeResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),

    # Pages
    url(r'^about/$', 'pages.views.about', name='pages_about'),
    url(r'^contact/$', 'pages.views.contact', name='pages_contact'),
    url(r'^tis/$', 'pages.views.tis', name='pages_tis'),
    url(r'^$', 'pages.views.home', name='home'),

    # Don't want to show account listing yet
    url('^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('katelinks.urls')),
    url(r'^mobile_apps/', include('mobile_apps.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^standards/', include('standards.urls')),
    url(r'^tick/', include('tick.urls')),

    url(r'^robots\.txt', 'pages.views.robot'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
