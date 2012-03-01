from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/$',
        'mobile_apps.views.view',
        name='mobile_apps_view'),

    url(r'^$',
        'mobile_apps.views.index',
        name='mobile_apps_index'),


)