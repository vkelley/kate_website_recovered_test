from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from resources.models import PdResource

def view(request, id):
	pdresource = get_object_or_404(PdResource, pk=id)
	return render_to_response("resources/pdresource/view.html",
							  {'pdresource': pdresource},
							  context_instance=RequestContext(request))