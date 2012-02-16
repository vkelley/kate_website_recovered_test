from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^search/$',
        'tick.views.search',
        name='tick_search'),

    url(r'^resource/(?P<id>\d+)/$',
        'tick.views.view',
        name='tick_resource'),
        
	url(r'^$',
		'tick.views.index',
		name='tick_index'),
)