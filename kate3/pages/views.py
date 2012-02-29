from django.shortcuts import render_to_response
from django.template import RequestContext

from logger.models import Entry
from tick.models import Announcement, Notice

def home(request):
    recent_resources = Entry.objects.get_for_model('tick', 'resource', action='Published')[0:4]
    tick_prize = Notice.objects.latest('created_at')
    tick_news = Announcement.objects.latest('created_at')
    return render_to_response('pages/home.haml',
                              {'recent_resources': recent_resources, 'tick_prize': tick_prize,
                               'tick_news': tick_news},
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('pages/about.haml',
                              context_instance=RequestContext(request))

def contact(request):
    return render_to_response('pages/contact.haml',
                              context_instance=RequestContext(request))

def tis(request):
    return render_to_response('pages/tis.haml',
                              context_instance=RequestContext(request))

def robot(request):
    return render_to_response('pages/robots.txt', mimetype='text/plain')
