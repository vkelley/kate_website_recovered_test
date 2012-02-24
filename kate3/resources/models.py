from django.contrib.auth.models import User
from django.db import models

class PdResource(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User)
    filename = models.FileField(upload_to="pdresource", blank=True, null=True)
    created = models.DateField(auto_now=True)
    sub_page = models.BooleanField(default=False, help_text="If this is checked, the link for this page will not show on the main PD Resource page.")

    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return ('resources_pdresource', (), {'id': self.id,})
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        verbose_name = "Professional Development Resource"
        ordering = ['title']

class EdResourceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return ('resources_edresource_category', (), {'id': self.id,})
    get_absolute_url = models.permalink(get_absolute_url)

class EdResource(models.Model):
    category = models.ForeignKey(EdResourceCategory)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(verify_exists=False)

    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = "Educational Resource"
        ordering = ['title',]

class TutorialCategory(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return ('resources_tutorial_category', (), {'id': self.id,})
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        verbose_name_plural = "Tutorial Categories"
        ordering = ['name',]

class Tutorial(models.Model):
    category = models.ForeignKey(TutorialCategory)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField()

    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.link

    class Meta:
        ordering = ['title',]