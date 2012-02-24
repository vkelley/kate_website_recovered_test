from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from resources.models import EdResourceCategory

def view(request, id):
	context = {
		'edresource_category': get_object_or_404(EdResourceCategory, pk=id),
		'edresource_categories': EdResourceCategory.objects.all(),
	}
	return render_to_response("resources/edresource/view.haml",
							  context,
							  context_instance=RequestContext(request))