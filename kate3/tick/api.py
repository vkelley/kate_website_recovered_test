from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource
from tastypie import fields

from tick.models import Resource, TechnologyStandard

class ResourceResource(ModelResource):
	class Meta:
		queryset = Resource.objects.all()
		resource_name = 'resource'
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()

class TechnologyStandardResource(ModelResource):
    class Meta:
        queryset = TechnologyStandard.objects.all()
        resource_name = 'tech_standard'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()