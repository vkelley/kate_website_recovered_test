from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

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

