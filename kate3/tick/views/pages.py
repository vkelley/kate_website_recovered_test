import locale

from django.shortcuts import render_to_response
from django.template import RequestContext

from tick.forms.search import FullSearchForm
from tick.models import Announcement, Notice, Resource

def index(request):
    if request.GET.has_key('keyword'):
        form = FullSearchForm(request.GET)
    else:
        form = FullSearchForm()

    context = {
        'announcement': Announcement.objects.latest('created_at'),
        'notice': Notice.objects.latest('created_at'),
        'form': form,
    }

    return render_to_response('tick/pages/index.haml',
                              context,
                              context_instance=RequestContext(request))

def about(request):
    locale.setlocale(locale.LC_ALL, "")
    count = Resource.public_objects.count()
    # If the count is greater than 100, we round down to the nearest 100.
    # That way we can say, "we have over 3100 resources" when we have 3102.
    if count > 100:
        count = int(count/100) * 100
    count = locale.format('%d', count, True)
    return render_to_response('tick/pages/about.haml',
                              {'count': count},
                              context_instance=RequestContext(request)) 

def news(request):
    announcement = Announcement.objects.latest('created_at')
    return render_to_response('tick/pages/news.haml',
                              {'announcement': announcement},
                              context_instance=RequestContext(request))

def prizes(request):
    notice = Notice.objects.latest('created_at')
    return render_to_response('tick/pages/prizes.haml',
                              {'notice': notice},
                              context_instance=RequestContext(request))