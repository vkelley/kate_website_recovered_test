from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from userena import views as userena_views

from accounts.forms import EditFormExtra

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tick/', include('tick.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
