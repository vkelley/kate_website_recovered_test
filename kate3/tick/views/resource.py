from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import ContentArea, Level
from tick.models import *
from tick.forms.search import FullSearchForm
from tick.forms.resource import ResourceEditForm

from utils.get_url import get_url

def search(request):
    get_request = request.GET.copy()

    for item, value in get_request.items():
        if get_request[item] == "all":
                del get_request[item]

    # See if the form is valid
    form = FullSearchForm(get_request)

    if form.is_valid():
        resources = Resource.public_objects.advanced_search(**form.cleaned_data)
    else:
        return HttpResponseRedirect(reverse('tick_index'))

    keyword = form.cleaned_data['keyword']
    
    paginator = Paginator(resources, 15)
    page = int(request.GET.get('page', 1))

    context = {
        'resources': paginator.page(page).object_list,
        'this_page': paginator.page(page),
        'paginator': paginator,
        'page': page,
        'get_request': get_request,
        'url': get_url(request),
        'keyword': keyword,
        'form_level': form.cleaned_data['levels'],
        'form_content_area': form.cleaned_data['content_areas'],
        'levels': Level.objects.all(),
        'content_areas': ContentArea.objects.all(),
    }

    return render_to_response('tick/resource/list.haml',
                              context,
                              context_instance=RequestContext(request))

def view(request, id):
    resource = get_object_or_404(Resource, pk=id)
    favorite = None
    if request.user.is_authenticated():
        favorites = Favorite.objects.filter(resource=resource,
                                           user=request.user)
        if favorites:
            favorite = favorites[0]
    return render_to_response('tick/resource/view.haml',
                              {'resource': resource, 'favorite': favorite},
                              context_instance=RequestContext(request))

@login_required
def submitted(request):
    resources = Resource.objects.filter(user=request.user).order_by('-created')
    return render_to_response('tick/resource/submitted.haml',
                              {'resources': resources},
                              context_instance=RequestContext(request))

@login_required
def edit(request, id):
    # Resource must exist and not be published
    try:
        resource = Resource.objects.get(pk=id, user=request.user, published=False)
    except Resource.DoesNotExist:
        return HttpResponseRedirect(reverse('tick_index'))

    if request.method == 'POST':
        form = ResourceEditForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message='Your resource was updated')
            return HttpResponseRedirect(reverse('tick_submitted'))
    else:
        form = ResourceEditForm(instance=resource)
    return render_to_response('tick/resource/edit.haml', {'form': form, 'resource': resource},
                            context_instance=RequestContext(request))

areas = {
    'math': 1,
    'reading': 6,
    'writing': 7,
    'lang_arts': 8,
}   

def core_content_ajax(request):
    """
    On step 2 of the submission process, when ``ContentArea``s are selected,
    an AJAX call is made to this view to display what ``CoreContent``s to
    allow the ``User`` to click.  
    
    Returns a string of options for core contents, separated by a new
    line and sent with a mimetype of 'text/javascript'.
    """
    if request.GET['content_area'] == 'null':
        return HttpResponse("", mimetype="text/html")
    
    options = []
    
    ids = list(map(int, request.GET['content_area'].split('_')))
    
    # Remove all the areas that are in the new Common Core Standards
    for area in areas.values():
        if area in ids:
            ids.remove(area)
            
    if len(ids) == 0:
        return HttpResponse("", mimetype="text/html")
    else:
        core_contents = CoreContent.objects.filter(content_area__id__in=ids)
    for c in core_contents:
        options.append('<option value="%s">%s</option>' % (c.id, c.code))
    return HttpResponse("\n".join(options), mimetype="text/javascript")

def common_core_ajax(request):
    """
    When submitting a resource, we filter down the Common Core Standards (``CommonCoreStandard``).
    This is done when a ``ContentArea`` is clicked on step 2 of the process, all by
    way of an AJAX call.  This view gets the ``ContentArea`` ids and selects the
    available common core standards based off of them.  This is done with jQuery.
    
    Returns a string of options for programs of study, separated by a new
    line and sent with a mimetype of 'text/javascript'.
    """
    # These are the primary keys of the content areas we need. We only have (as of 1/1/11)
    # the common core standards for math, reading, and writing.
    
    if request.GET['content_area'] == 'null':
        return HttpResponse("", mimetype="text/javascript")
    
    # These are the submitted IDs for the content areas
    ids = tuple(map(int, request.GET['content_area'].split('_')))
    #common_cores = tuple(map(int, request.GET['common_core'].split('_')))
    
    # All of the records from 1-488 are math. The rest are Reading/Language Arts
    if areas['math'] in ids and (areas['reading'] in ids or areas['writing'] in ids or areas['lang_arts'] in ids):
        standards = CommonCoreStandard.objects.all()
    elif areas['math'] in ids:
        standards = CommonCoreStandard.objects.filter(id__range=(1,488))
    elif areas['reading'] in ids or areas['writing'] in ids or areas['lang_arts'] in ids:
        standards = CommonCoreStandard.objects.filter(id__gt=488)
    else:
        standards = CommonCoreStandard.objects.none()
    
    # This builds the option list
    options = []
    
    for s in standards:
        options.append('<option value="%s">%s</option>' % (s.id, s.name))
        
    return HttpResponse("\n".join(options), mimetype="text/javascript")