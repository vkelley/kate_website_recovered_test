from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from core.models import ContentArea, Level
from tick.models import CommonCoreStandard, Resource, TechnologyStandard

class BaseResourceResource(ModelResource):
    content_areas = fields.ToManyField('tick.api.ContentAreaResource', 'content_areas', full=True)
    levels = fields.ToManyField('tick.api.LevelResource', 'levels', full=True)
    url = fields.CharField(readonly=True)

    def obj_get_list(self, request, *args, **kwargs):
        resources = super(BaseResourceResource, self).obj_get_list(request, *args, **kwargs)
        if request.GET.has_key('search'):
            return resources.advanced_search(keyword=request.GET['search'])
        return resources

    class Meta:
        queryset = Resource.public_objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get',]

        fields = ['id', 'title', 'description', 'source', 'url',
                  'aligned_to_common_core']

        resource_name = 'tick_resource'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        filtering = {
            'aligned_to_common_core': ['exact',],
        }

    def dehydrate_url(self, bundle):
        return bundle.obj.get_full_url()

class ResourceResource(BaseResourceResource):
    common_cores = fields.ToManyField('tick.api.BaseCommonCoreResource', 'common_core_standards', full=True)

class BaseCommonCoreResource(ModelResource):
    class Meta:
        queryset = CommonCoreStandard.objects.all()
        fields = ['name', 'description']
        resource_name = 'common_core'

class CommonCoreResource(BaseCommonCoreResource):
    tick_resources = fields.ToManyField(BaseResourceResource, 'resource_set', full=True)

class LevelResource(ModelResource):
    class Meta:
        queryset = Level.objects.all()
        fields = ['name',]
        include_resource_uri = False
        filtering = {
            'name': ['exact',]
        }

class ContentAreaResource(ModelResource):
    class Meta:
        queryset = ContentArea.objects.all()
        include_resource_uri = False
        filtering = {
            'name': ['exact',]
        }

class TechnologyStandardResource(ModelResource):
    class Meta:
        queryset = TechnologyStandard.objects.all()
        resource_name = 'tech_standard'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()