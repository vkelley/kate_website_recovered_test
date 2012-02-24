from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from tick.models import *
from tick.forms.submit import ResourceStep1Form, ResourceStep2Form

@login_required
def step_1(request):
    if request.method == 'POST':
        form = ResourceStep1Form(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(user=request.user)
            request.user.message_set.create(message='Step 1 was successful')
            return HttpResponseRedirect(reverse('tick_submit_step_2', args=[resource.id]))
    else:
        form = ResourceStep1Form()
    return render_to_response('tick/submit/step_1.haml', {'form': form},
                              context_instance=RequestContext(request))

@login_required
def step_2(request, id):
    try:
        resource = Resource.objects.get(pk=id, user=request.user, published=False)
    except Resource.DoesNotExist:
        return HttpResponseRedirect(reverse('tick_index'))

    if request.method == 'POST':
        form = ResourceStep2Form(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message='Thank you! Your resource was submitted and will be evaluated. We will notify you if your resource is published.')
            return HttpResponseRedirect(reverse('tick_index'))
    else:
        form = ResourceStep2Form(instance=resource)
    return render_to_response('tick/submit/step_2.haml', {'form': form, 'resource': resource},
                              context_instance=RequestContext(request))