from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$',
		'standards.views.index',
		name='standards_index'),

	url(r'^core_content/(?P<subject>[A-Z]{2})/$',
		'standards.views.core_content',
		name='standards_corecontent'),
)