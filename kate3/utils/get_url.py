from django.conf import settings

def get_url_seth(request, exclude_fields=['page', 'areas'], multiple_fields=['areas']):
    """
    This is Seth Buntin's version.  I am keeping it around in case I need it. As
    of right now, this isn't used anywhere.
    
    This grabs all the items in the request.GET dict that is not
    the page varaible and makes it into a url string that the
    pagination templatetag uses along with other search links.
    """
    string = '&'.join(['%s=%s' % (k, v) for k,v in request.GET.items() if k not in exclude_fields and v != ''])
    for field in multiple_fields:
        if field in request.GET:
            for item in request.GET.getlist(field):
                string += "&%s=%s" % (field, item)
    return string


def get_url(request, fields=settings.URL_EXCLUDE_FIELDS):
    """
    This grabs all the items in the request.GET dict that is not
    the page varaible and makes it into a url string that the
    pagination templatetag uses along with other search links.
    
    This one-liner splits all of the GET items, loops through them, checks to see if
    they are in ``URL_EXCLUDED_FIELDS`` list or if they're empty, and, if not, puts
    them into a list with ``key=value``.  It then joins each item in that list
    by the &.
    """
    return '&'.join(['%s=%s' % (k, v) for k,v in request.GET.items() if k not in fields and v != ''])
