from django.shortcuts import render_to_response

def robot(request):
	return render_to_response('pages/robots.txt', mimetype='text/plain')
