from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from userena import views as userena_views

from accounts.forms import EditFormExtra, SignupFormExtra

admin.autodiscover()

urlpatterns = patterns('',

    
    url(r'^signup/$',
       userena_views.signup,
       {'signup_form': SignupFormExtra},
       name='userena_signup'),

    url(r'^(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit,
       {'edit_profile_form': EditFormExtra},
       name='userena_profile_edit'),

    url(r'', include('userena.urls')),

)