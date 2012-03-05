from django.contrib.syndication.feeds import Feed
from django.contrib.contenttypes.models import ContentType

from logger.models import Entry, Action
from tick.models import Resource

class RecentlyPublishedFeed(Feed):
    title = "Recently Published on TICK"
    link = "/tick/"
    description = "Recently published resources on TICK"
    
    def items(self, obj):
        return Entry.objects.filter(content_type=ContentType.objects.get(app_label='tick', model='resource'),
                                    action=Action.objects.get(name='Published'))[:10]