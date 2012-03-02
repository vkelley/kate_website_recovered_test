from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import ContentArea, Level
from mobile_apps.models import App, Type

def index(request):
    apps = App.objects.filter(published=True)
    levels = Level.objects.all()
    content_areas = ContentArea.objects.all()
    types = Type.objects.all()
    return render_to_response('mobile_apps/index.haml',
                              {'apps': apps, 'levels': levels, 
                               'content_areas': content_areas,
                               'types': types},
                              context_instance=RequestContext(request))

def view(request, id):
    app = get_object_or_404(App, pk=id, published=True)
    levels = Level.objects.all()
    content_areas = ContentArea.objects.all()
    types = Type.objects.all()
    return render_to_response('mobile_apps/view.haml',
                              {'app': app, 'levels': levels, 
                               'content_areas': content_areas,
                               'types': types},
                              context_instance=RequestContext(request))