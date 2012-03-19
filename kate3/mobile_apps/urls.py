from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/$',
        'mobile_apps.views.view',
        name='mobile_apps_view'),

    url(r'^submit/$',
        'mobile_apps.views.submit',
        name='mobile_apps_submit'),

    url(r'^$',
        'mobile_apps.views.index',
        name='mobile_apps_index'),


)