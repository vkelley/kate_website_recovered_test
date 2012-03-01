from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from userena import views as userena_views

from accounts.forms import EditFormExtra

admin.autodiscover()

urlpatterns = patterns('',

    # Pages
    url(r'^about/$', 'pages.views.about', name='pages_about'),
    url(r'^contact/$', 'pages.views.contact', name='pages_contact'),
    url(r'^tis/$', 'pages.views.tis', name='pages_tis'),
    url(r'^$', 'pages.views.home', name='home'),

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
