from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import *

from tick.models import *
from tick.forms.search import FullSearchForm

from utils.get_url import get_url

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

    return render_to_response('tick/index.haml',
                              context,
                              context_instance=RequestContext(request))

def search(request):
    # See if the form is valid
    form = FullSearchForm(request.GET)
    if form.is_valid():
        resources = Resource.public_objects.advanced_search(**form.cleaned_data)
    else:
        print form
        return HttpResponse('hey')
    
    paginator = Paginator(resources, 15)
    page = int(request.GET.get('page', 1))

    context = {
        'resources': paginator.page(page).object_list,
        'this_page': paginator.page(page),
        'paginator': paginator,
        'page': page,
        'url': get_url(request)
    }

    return render_to_response('tick/resource_list.haml',
                              context,
                              context_instance=RequestContext(request))

def view(request, id):
    resource = get_object_or_404(Resource, pk=id)
    return render_to_response('tick/resource_detail.haml',
                              {'resource': resource},
                              context_instance=RequestContext(request))

    
