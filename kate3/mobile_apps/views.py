from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import ContentArea, Level
from mobile_apps.models import App, Type
from mobile_apps.forms import AppForm

def index(request):
    apps = App.objects.filter(published=True)

    filtered = False

    if request.GET.has_key('free'):
        if request.GET['free'] == "1":
            apps = apps.filter(cost='0.00')
        elif request.GET['free'] == "0":
            apps = apps.exclude(cost='0.00')
        filtered = True

    if request.GET.has_key('type'):
        apps = apps.filter(type__id=request.GET['type'])
        filtered = True

    if request.GET.has_key('levels'):
        apps = apps.filter(levels__id=request.GET['levels'])
        filtered = True

    if request.GET.has_key('content_areas'):
        apps = apps.filter(content_areas__id=request.GET['content_areas'])
        filtered = True

    levels = Level.objects.all()
    content_areas = ContentArea.objects.all()
    types = Type.objects.all()
    return render_to_response('mobile_apps/index.haml',
                              {'apps': apps, 'levels': levels, 
                               'content_areas': content_areas,
                               'types': types, 'filtered': filtered},
                              context_instance=RequestContext(request))

def submit(request):
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            request.user.message_set.create(message='Your app was submitted!')
            return HttpResponseRedirect(reverse('mobile_apps_index'))
    else:
        form = AppForm()
    return render_to_response('mobile_apps/submit.haml',
                              {'form': form},
                              context_instance=RequestContext(request))

def view(request, id):
    app = get_object_or_404(App, pk=id, published=True)
    return render_to_response('mobile_apps/view.haml',
                              {'app': app},
                              context_instance=RequestContext(request))