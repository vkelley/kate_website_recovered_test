from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from userena import views as userena_views

from accounts.forms import EditFormExtra

admin.autodiscover()

urlpatterns = patterns('',

    # Accounts URLs
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit,
       {'edit_profile_form': EditFormExtra},
       name='userena_profile_edit'),

    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tick/', include('tick.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
