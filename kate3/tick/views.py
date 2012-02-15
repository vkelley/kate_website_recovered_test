from django.shortcuts import render_to_response

from tick.models import *
from tick.forms.search import FullSearchForm

def index(request):
    context = {
        'announcement': Announcement.objects.latest('created_at'),
        'notice': Notice.objects.latest('created_at'),
        'form': FullSearchForm(),
    }
    return render_to_response('tick/index.haml', context)
