from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

	# PD Resources
	url(r'^pdresource/(?P<id>\d+)/$',
        'resources.views.pdresource.view',
        name='resources_pdresource'),

	url(r'^pdresource/$',
        'resources.views.pdresource.list',
        name='resources_pdresource_list'),

	# Training and Tutorials
	url(r'^tutorials/(?P<id>\d+)/$',
        'resources.views.tutorial.view',
        name='resources_tutorial_category'),

	# Educational Resources
	url(r'^edu_resource/(?P<id>\d+)/$',
        'resources.views.edresource.view',
        name='resources_edresource_category'),

	# Index page
	url(r'^$',
        'resources.views.index',
        name='resources_index'),
)