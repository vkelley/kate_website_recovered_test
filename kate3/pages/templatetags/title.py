from django import template

from django.conf import settings

register = template.Library()

class SetTitle(template.Node):

    def __init__(self, titles=None):
        self.titles = titles
    
    def render(self, context):
        if self.titles:
            return " - ".join(self.titles)
        return self.site_title

@register.tag
def title(parser, token):
    bits = token.split_contents()

    titles = [settings.SITE_TITLE,]

    if len(bits) > 1:
        title_list = bits[1:]

        for title in title_list:
            if not (title[0] == title[-1] and title[0] in ('"', "'")):
                raise template.TemplateSyntaxError("%s tag's arguments should be in quotes" % bits[0])
            titles.append(title[1:-1])

        if getattr(settings, "REVERSE_TITLE", False):
            titles.reverse()

    return SetTitle(titles)