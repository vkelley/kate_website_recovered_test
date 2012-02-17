from django import template

from tick.models import Resource

register = template.Library()

class UserResources(template.Node):

    def __init__(self, user):
        self.user = user

    def render(self, context):
        context['user_resources'] = Resource.public_objects.filter(user=self.user)
        return ''

@register.tag
def get_user_resources(parser, token):
    tag_name, user = token.split_contents()
    return UserResources(user)