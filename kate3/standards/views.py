from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from tick.models import CoreContent
from standards.forms import SearchForm
from standards.models import Subject, Cluster, Category, Subcategory, CommonCoreStandard

CORE_CONTENT_LIST = {
    'AH': {'id': 5, 'title': 'Arts &amp; Humanities'},
    'MA': {'id': 1, 'title': 'Mathematics'},
    'PL': {'id': 4, 'title': 'Practical Living/Vocational Studies'},
    'RE': {'id': 6, 'title': 'Reading'},
    'SC': {'id': 3, 'title': 'Science'},
    'SS': {'id': 2, 'title': 'Social Studies'},
    'WR': {'id': 7, 'title': 'Writing'},
}

COMMON_CORE_LIST = {
  'MA': {'id': 1, 'title': 'Mathematics'},
  'LA': {'id': 2, 'title': 'English Language Arts'},
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

def common_core_index(request):
    context = {
        'subjects': Subject.objects.all().order_by('name'),
        'categories': Category.objects.all().order_by('name'),
        'subcategories': Subcategory.objects.all().order_by('name'),
        'math': Subject.objects.get(id=1),
        'language': Subject.objects.get(id=2),
        'form': SearchForm(),
    }
    return render_to_response('standards/common_core_index.haml',
                  context,
                  context_instance=RequestContext(request))

def common_core_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        common_core = CommonCoreStandard.objects.all()

        if form.is_valid():

            if form.cleaned_data['keyword']:
                common_core = common_core.filter(Q(description__contains=form.cleaned_data['keyword']) | \
                             Q(description__contains=form.cleaned_data['keyword']))

            if form.cleaned_data['standard']:
                common_core = common_core.filter(standard_code=form.cleaned_data['standard'])

            if form.cleaned_data['subject']:
                common_core = common_core.filter(subject=form.cleaned_data['subject'])

            if form.cleaned_data['grade']:
                common_core = common_core.filter(grade=form.cleaned_data['grade'])

            if form.cleaned_data['category']:
                common_core = common_core.filter(category=form.cleaned_data['category'])

            if form.cleaned_data['subcategory']:
                common_core = common_core.filter(subcategory=form.cleaned_data['subcategory'])

            if form.cleaned_data['cluster']:
                common_core = common_core.filter(cluster=form.cleaned_data['cluster'])

            return render_to_response('standards/common_core_search.haml',
                                      {'common_core': common_core, 'form': form},
                                      context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect(reverse('common_core_index'))


def common_core_subject(request, subject):
  common_core_subjects = CommonCoreStandard.objects.filter(subject__exact=COMMON_CORE_LIST[subject]['id']).order_by('grade', 'standard_code')
  categories = Category.objects.all()

  return render_to_response('standards/common_core_subject.haml',
                              {'common_core_subjects': common_core_subjects,
                              'title': COMMON_CORE_LIST[subject]['title']},
                              context_instance=RequestContext(request))

def cat_subcat_view(request, category_id=None, subcategory_id=None):
    category = get_object_or_404(Category, pk=category_id)
    standards = CommonCoreStandard.objects.filter(category=category_id)

    subcategory=None
    if subcategory_id:
      subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
      standards = CommonCoreStandard.objects.filter(subcategory=subcategory_id)

    context = {
      'standards': standards,
      'category': category,
      'subcategory': subcategory,
      'categories': Category.objects.all(),
      'subcategories': Subcategory.objects.all(),
    }

    return render_to_response('standards/common_core_cat_detail.haml',
                                context,
                                context_instance=RequestContext(request))

def common_core_detail(request, standard_code):
    standard = CommonCoreStandard.objects.get(standard_code=standard_code)

    return render_to_response('standards/common_core_detail.haml',
                                {'standard': standard}, context_instance=RequestContext(request))