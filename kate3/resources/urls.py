from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^pd/(?P<id>\d+)/$',
        'resources.views.pdresource.view',
        name='tick_pdresource'),
)