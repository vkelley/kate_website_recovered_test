from django.shortcuts import render_to_response
from django.template import RequestContext

from tick.models import CoreContent

CORE_CONTENT_LIST = {
    'AH': {'id': 5, 'title': 'Arts &amp; Humanities'},
    'MA': {'id': 1, 'title': 'Mathematics'},
    'PL': {'id': 4, 'title': 'Practical Living/Vocational Studies'},
    'RE': {'id': 6, 'title': 'Reading'},
    'SC': {'id': 3, 'title': 'Science'},
    'SS': {'id': 2, 'title': 'Social Studies'},
    'WR': {'id': 7, 'title': 'Writing'},
}

def index(request):
    return render_to_response('standards/index.haml',
                              {'core_contents': CoreContent.objects.all(),},
                              context_instance=RequestContext(request))

def core_content(request, subject):
    core_contents = CoreContent.objects.filter(subject__exact=CORE_CONTENT_LIST[subject]['id']).order_by('level','bigidea','subcategory','catpoint')
    
    return render_to_response('standards/core_content.haml',
                              {'core_contents': core_contents, 
                               'title': CORE_CONTENT_LIST[subject]['title']},
                              context_instance=RequestContext(request))



