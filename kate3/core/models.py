from django.db import models

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
