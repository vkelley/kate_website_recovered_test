from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	
	url(r'^$',
		'standards.views.index',
		name='standards_index'),

	url(r'^core_content/(?P<subject>[A-Z]{2})/$',
		'standards.views.core_content',
		name='standards_corecontent'),

	url(r'^common_core/$',
        'standards.views.common_core_index',
        name='common_core_index'),

	url(r'^common_core/search/$',
		'standards.views.common_core_search',
		name='common_core_search'),

	url(r'^common_core/(?P<subject>[A-Z]{2})/$',
		'standards.views.common_core_subject',
		name='common_core_subject'),

	url(r'^common_core/category/(?P<category_id>\d+)/$',
    	    'standards.views.cat_subcat_view',
        	name='category_view'),

	url(r'^common_core/category/(?P<category_id>\d+)/subcategory/(?P<subcategory_id>\d+)/$',
	        'standards.views.cat_subcat_view',
	        name='subcategory_view'),

	url(r'^common_core/(?P<standard_code>.*)/$',
		'standards.views.common_core_detail',
		name='common_core_detail'),
)