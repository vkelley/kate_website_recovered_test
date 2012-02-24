from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from katelinks.forms import SearchForm
from katelinks.models import Category, Focus, Level, Link, Title

def index(request):
    context = {
        'categories': Category.objects.all().order_by('name'),
        'levels': Level.objects.all(),
        'focuses': Focus.objects.all(),
    	'art': Title.objects.get(id=1),
        'math': Title.objects.get(id=2),
        'practical': Title.objects.get(id=3),
        'reading': Title.objects.get(id=4),
        'science': Title.objects.get(id=5),
        'social': Title.objects.get(id=6),
        'writing': Title.objects.get(id=7),
        'other': Title.objects.get(id=8),
        'web': Title.objects.get(id=9),
        'form': SearchForm(),
    }
    return render_to_response('katelinks/index.haml',
    						  context,
    						  context_instance=RequestContext(request))

def view(request, category_id=None, level_id=None):
    category = get_object_or_404(Category, pk=category_id)
    links = Link.objects.filter(categories=category.id)

    level = None
    if level_id:
        level = get_object_or_404(Level, pk=level_id)
        links = links.filter(level=level.id)

    context = {
        'links': links,
        'category': category,
        'level': level,
        'levels': Level.objects.all(),
    }

    return render_to_response('katelinks/view.haml',
                              context,
                              context_instance=RequestContext(request))

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        links = Link.objects.all()

        if form.is_valid():

            if form.cleaned_data['keyword']:
                links = links.filter(Q(title__contains=form.cleaned_data['keyword']) | \
                             Q(description__contains=form.cleaned_data['keyword']))

            if form.cleaned_data['category']:
                links = links.filter(categories=form.cleaned_data['category'])

            if form.cleaned_data['level']:
                links = links.filter(level=form.cleaned_data['level'])

            if form.cleaned_data['focus']:
                links = links.filter(focus=form.cleaned_data['focus'])

            return render_to_response('katelinks/search.haml',
                                      {'links': links, 'form': form},
                                      context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect(reverse('katelinks_index'))

