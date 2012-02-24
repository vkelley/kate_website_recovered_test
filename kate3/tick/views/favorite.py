from tagging.models import Tag, TaggedItem
from tagging.utils import edit_string_for_tags

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from tick.models import Favorite, Resource
from tick.forms.favorite import AddFavoriteForm, EditFavoriteForm

@login_required
def list(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    tags = Tag.objects.usage_for_queryset(favorites)
    return render_to_response('tick/favorite/list.haml', 
                              {'favorites': favorites, 'tags': tags}, 
                              context_instance=RequestContext(request))

@login_required
def list_by_tag(request, tag_id):
    favorites = Favorite.objects.filter(user=request.user)
    tags = Tag.objects.usage_for_queryset(favorites)
    tag = Tag.objects.get(pk=tag_id)
    favorites = TaggedItem.objects.get_by_model(Favorite, tag).filter(user=request.user).order_by('-created_at')
    return render_to_response('tick/favorite/list_by_tag.haml',
                              {'favorites': favorites, 'tag': tag, 'tags': tags},
                              context_instance=RequestContext(request))

@login_required
def add(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    if request.method == 'POST':
        form = AddFavoriteForm(request.POST)
        if form.is_valid():
            form.save(request, resource)
            request.user.message_set.create(message='Your favorite was created')
            return HttpResponseRedirect(reverse('tick_favorite_list'))
    form = AddFavoriteForm()
    return render_to_response('tick/favorite/add.haml',     
                              {'form': form, 'resource': resource},
                              context_instance=RequestContext(request))

@login_required
def edit(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id, user=request.user)
    if request.method == 'POST':
        form = EditFavoriteForm(request.POST)
        if form.is_valid():
            form.save(favorite)
            request.user.message_set.create(message='Your favorite was updated')
            return HttpResponseRedirect(reverse('tick_favorite_list'))
    form = EditFavoriteForm({'notes': favorite.notes,
                         'tags': edit_string_for_tags(favorite.tags)})
    return render_to_response('tick/favorite/edit.haml', 
                              {'form': form, 'resource': favorite.resource, 'favorite': favorite},
                              context_instance=RequestContext(request))

def delete(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id, user=request.user)
    favorite.delete()
    request.user.message_set.create(message='Your favorite was deleted')
    return HttpResponseRedirect(reverse('tick_favorte_list'))