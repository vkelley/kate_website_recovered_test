import urllib

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    productivity = False

    get_request = request.GET.copy()

    for item, value in get_request.items():
        if get_request[item] == "all":
            del get_request[item]

    for item in ['type', 'levels', 'content_areas']:
        if get_request.has_key(item):
            get_request[item] = int(get_request[item])

    if get_request.has_key('free'):
        if request.GET['free'] == "1":
            apps = apps.filter(cost='0.00')
        elif request.GET['free'] == "0":
            apps = apps.exclude(cost='0.00')
        filtered = True

    if get_request.has_key('type'):
        apps = apps.filter(type__id=request.GET['type'])
        filtered = True

    if get_request.has_key('productivity'):
        if get_request['productivity'] == "1":
            apps = apps.filter(productivity=True)
            productivity = True
        else:
            apps = apps.filter(productivity=False)
        filtered = True

    if get_request.has_key('levels'):
        apps = apps.filter(levels__id=request.GET['levels'])
        filtered = True

    if get_request.has_key('content_areas'):
        apps = apps.filter(content_areas__id=request.GET['content_areas'])
        filtered = True

    paginator = Paginator(apps, 10)
    page = int(request.GET.get('page', 1))

    levels = Level.objects.all()
    content_areas = ContentArea.objects.all()
    types = Type.objects.all()

    context = {
        'apps': paginator.page(page).object_list,
        'this_page': paginator.page(page),
        'paginator': paginator,
        'page': page,
        'get_request': get_request,
        'levels': levels, 
        'content_areas': content_areas,
        'types': types,
        'filtered': filtered,
        'productivity': productivity,
    }

    return render_to_response('mobile_apps/index.haml',
                              context,
                              context_instance=RequestContext(request))

@login_required
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