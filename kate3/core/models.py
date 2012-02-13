from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User)
    levels = models.ManyToManyField('Level', blank=True)
    content_areas = models.ManyToManyField('ContentArea', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class ContentArea(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']

class Level(models.Model):
    """
    Level, which is the grade
    """
    name = models.CharField(max_length=25)
    level = models.CharField(max_length=45)
    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['order']
