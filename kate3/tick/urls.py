from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$',
		'tick.views.index',
		name='tick_index'),
)