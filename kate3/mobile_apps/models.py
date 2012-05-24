from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

import itunes

from core.models import ContentArea, Level
from utils.google_play import GetAppInfo

class Type(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.ForeignKey(Type)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    link = models.URLField(max_length=200, verify_exists=True, blank=True, null=True)
    levels = models.ManyToManyField(Level, blank=True, null=True)
    content_areas = models.ManyToManyField(ContentArea, blank=True, null=True)

    productivity = models.BooleanField()

    user = models.ForeignKey(User, blank=True, null=True)
    published = models.BooleanField()

    educational_uses = models.TextField(blank=True)

    store_name = models.CharField(max_length=200, blank=True)
    store_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    #store_description = models.TextField(blank=True)
    store_link = models.URLField(max_length=200, verify_exists=True, blank=True, null=True)
    store_avg_rating = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    store_num_ratings = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s for %s" % (self.name, self.type)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
            self.get_itunes_info()
            self.get_android_info()
        super(App, self).save(*args, **kwargs)

    def get_itunes_info(self):
        if self.type.name == 'iOS':
            try:
                item = itunes.search(query=self.name, media='software')[0]
                self.store_name = item.name
                self.store_cost = item.price
                #self.store_description = unicode(item.get_description()).encode('utf8')
                self.store_link = item.url
                self.store_avg_rating = item.avg_rating
                self.store_num_ratings = item.num_ratings
            except:
                pass

    def get_android_info(self):
        if self.type.name == 'Android':
            try:
                i = GetAppInfo(self.name)
                results = i.get_info()
                self.store_name = results['name']
                self.store_cost = results['cost']
                self.store_link = results['url']
            except:
                pass


    def for_all_levels(self):
        if self.levels.count() == Level.objects.count():
            return True
        return False

    def for_all_areas(self):
        if self.content_areas.count() == ContentArea.objects.count():
            return True
        return False