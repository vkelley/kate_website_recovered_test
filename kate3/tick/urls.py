from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    # Favorite Views
    url(r'^favorite/add/(?P<resource_id>\d+)/$',
        'tick.views.favorite.add',
        name='tick_favorite_add'),

    url(r'^favorite/edit/(?P<favorite_id>\d+)/$',
        'tick.views.favorite.edit',
        name='tick_favorite_edit'),

    url(r'^favorite/delete/(?P<favorite_id>\d+)/$',
        'tick.views.favorite.delete',
        name='tick_favorite_delete'),

    url(r'^favorite/tag/(?P<tag_id>\d+)/$',
        'tick.views.favorite.list_by_tag',
        name='tick_favorite_list_by_tag'),

    url(r'^favorite/$',
        'tick.views.favorite.list',
        name='tick_favorite_list'),

    # Resource Views
    url(r'^search/$',
        'tick.views.resource.search',
        name='tick_search'),

    url(r'^resource/(?P<id>\d+)/$',
        'tick.views.resource.view',
        name='tick_resource'),
        
    # Page Views

    url(r'^about/$',
        'tick.views.pages.about',
        name='tick_about'),
    
	url(r'^$',
		'tick.views.pages.index',
		name='tick_index'),
)