from decimal import Decimal

from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from mobile_apps.models import App, Type

class TypeResource(ModelResource):
    class Meta:
        resource_name = 'app_type'
        queryset = Type.objects.all()
        fields = ['name',]
        include_resource_uri = False
        filtering = {
            'name': ['exact',]
        }

        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class AppResource(ModelResource):
    content_areas = fields.ToManyField('tick.api.ContentAreaResource', 'content_areas', full=True)
    levels = fields.ToManyField('tick.api.LevelResource', 'levels', full=True)
    type = fields.ForeignKey(TypeResource, 'type')

    class Meta:
        queryset = App.objects.filter(published=True)
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get',]

        authentication = Authentication()
        authorization = Authorization()

        fields = ['name', 'description', 'educational_uses', 'cost', 'link']

        filtering = {
            'content_areas': ALL_WITH_RELATIONS,
            'levels': ALL_WITH_RELATIONS,
            'type': ALL_WITH_RELATIONS,
        }

        resource_name = 'mobile_app'

    def dehydrate_cost(self, bundle):
        if bundle.obj.cost == Decimal('0.00') or bundle.obj.cost == '':
            return 'Free'
        else:
            return '$%s' % bundle.obj.cost

    def dehydrate_type(self, bundle):
        return bundle.obj.type
