from django.conf.urls.defaults import patterns, include, url

from tick.feeds import RecentlyPublishedFeed

feeds = {
    'tick_recent': RecentlyPublishedFeed,
}

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

    url(r'^submitted/$',
        'tick.views.resource.submitted',
        name='tick_submitted'),

    url(r'^resource/(?P<id>\d+)/$',
        'tick.views.resource.view',
        name='tick_resource'),

    # Feeds
    url(r'^feeds/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds},
        name='tick_feed'),
    
    # Edit page
    #url(r'^resource/(?P<id>\d+)/edit/$',
    #    'tick.views.resource.edit',
    #    name='tick_resource_edit'),

    # Submission Process
    url(r'^submit/step1/$',
        'tick.views.submit.step_1',
        name='tick_submit_step_1'),

    url(r'^submit/step2/(?P<id>\d+)/$',
        'tick.views.submit.step_2',
        name='tick_submit_step_2'),

    # AJAX Views
    url(r'^core_content_ajax/$',
        'tick.views.resource.core_content_ajax',
        name='tick_core_content_ajax'),

    url(r'^common_core_ajax/$',
        'tick.views.resource.common_core_ajax',
        name='tick_common_core_ajax'),
        
    # Page Views
    url(r'^news/$',
        'tick.views.pages.news',
        name='tick_news'),

    url(r'^prizes/$',
        'tick.views.pages.prizes',
        name='tick_prizes'),

    url(r'^about/$',
        'tick.views.pages.about',
        name='tick_about'),
    
	url(r'^$',
		'tick.views.pages.index',
		name='tick_index'),
)
