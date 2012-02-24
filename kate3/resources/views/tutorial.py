from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from resources.models import TutorialCategory

def view(request, id):
	context = {
		'tutorial_category': get_object_or_404(TutorialCategory, pk=id),
		'tutorial_categories': TutorialCategory.objects.all(),
	}
	return render_to_response("resources/tutorial/view.haml",
							  context,
							  context_instance=RequestContext(request))