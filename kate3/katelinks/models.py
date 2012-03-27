from django.contrib.auth.models import User
from django.db import models

# At some point, these need to be rolled into the
# models used in TICK. They are the same thing,
# just used in two different places

class Level(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Focus(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Focuses'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Title(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.name

class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(verify_exists=True)
    description = models.TextField()
    created = models.DateField(auto_now=True)
    user = models.ForeignKey(User)
    categories = models.ManyToManyField(Category)
    level = models.ManyToManyField(Level)
    focus = models.ManyToManyField(Focus)

    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.url

    class Meta:
        ordering = ['title']
