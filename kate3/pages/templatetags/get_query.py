import urllib

from django import template
from django.conf import settings

register = template.Library()

class GetQuery(template.Node):

    def __init__(self, query_dict, key, value):
        self.query_dict = template.Variable(query_dict)
        self.key = key
        if value.startswith('"'):
            self.value = unicode(value[1:-1])
        else:
            self.value = template.Variable(value)

    def render(self, context):
        query_dict = self.query_dict.resolve(context).copy()

        for exclude_field in settings.URL_EXCLUDE_FIELDS:
            if query_dict.has_key(exclude_field):
                del query_dict[exclude_field]

        for item, value in query_dict.items():
            if query_dict[item] == "":
                del query_dict[item]

        if type(self.value) == unicode:
            query_dict[self.key] = self.value
        else:
            query_dict[self.key] = self.value.resolve(context)

        return urllib.urlencode(query_dict)

@register.tag
def get_query(parser, token):
    tag_name, query_dict, key, value = token.split_contents()
    return GetQuery(query_dict, key, value)