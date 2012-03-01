from datetime import datetime

from django.db import models

from core.models import ContentArea, Level

class Type(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    type = models.ForeignKey(Type)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    link = models.URLField(max_length=200, verify_exists=True)
    levels = models.ManyToManyField(Level, blank=True, null=True, related_name='levels')
    content_areas = models.ManyToManyField(Level, blank=True, null=True, related_name='content_areas')

    created_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s for %s" % (self.name, self.type)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        super(App, self).save(*args, **kwargs)