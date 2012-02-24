from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from resources.models import EdResourceCategory, PdResource, TutorialCategory

def index(request):
	context = {
		'pdresources': PdResource.objects.filter(sub_page=False),
		'edresource_categories': EdResourceCategory.objects.all(),
		'tutorial_categories': TutorialCategory.objects.all()
	}
	return render_to_response("resources/index.haml",
							  context,
							  context_instance=RequestContext(request))