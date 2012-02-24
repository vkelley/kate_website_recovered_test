from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from resources.models import PdResource

def view(request, id):
	pdresource = get_object_or_404(PdResource, pk=id)
	pdresources = PdResource.objects.filter(sub_page=False)
	return render_to_response("resources/pd/view.haml",
							  {'pdresource': pdresource, 'pdresources': pdresources},
							  context_instance=RequestContext(request))

def list(request):
	pdresources = PdResource.objects.filter(sub_page=False)
	return render_to_response("resources/pd/list.haml",
							  {'pdresources': pdresources},
							  context_instance=RequestContext(request))