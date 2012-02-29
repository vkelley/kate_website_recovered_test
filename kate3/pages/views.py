from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
	return render_to_response('pages/about.haml',
							  context_instance=RequestContext(request))

def contact(request):
	return render_to_response('pages/contact.haml',
							  context_instance=RequestContext(request))

def tis(request):
	return render_to_response('pages/tis.haml',
							  context_instance=RequestContext(request))

def robot(request):
	return render_to_response('pages/robots.txt', mimetype='text/plain')
