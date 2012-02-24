from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

	url(r'^(?P<category_id>\d+)/$',
        'katelinks.views.view',
        name='katelinks_category_view'),

	url(r'^(?P<category_id>\d+)/(?P<level_id>\d+)/$',
        'katelinks.views.view',
        name='katelinks_category_level_view'),

	url(r'search/$',
		'katelinks.views.search',
		name='katelinks_search'),

	url(r'^$',
        'katelinks.views.index',
        name='katelinks_index'),

)