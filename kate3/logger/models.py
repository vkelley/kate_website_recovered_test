from django.db import models

from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import Template, TemplateDoesNotExist, Context
from django.template.loader import render_to_string


class Action(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.name)

class EntryManager(models.Manager):
    """ Custom manager for Entry model """
    
    def get_status(self, action_string="New"):
        return Action.objects.get_or_create(name=action_string)[0]
        
    def get_for_model(self, app_label, model, action='New', order_by='-created_at'):
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            action = Action.objects.get(name=action)
            return Entry.objects.filter(content_type=content_type, action=action).order_by(order_by)
        except (ContentType.DoesNotExist, Action.DoesNotExist, Entry.DoesNotExist):
            return None
            
    def get_for_object(self, instance):
        try:
            content_type = ContentType.objects.get_for_model(instance)
            entries = Entry.objects.filter(content_type=content_type, object_id=instance.pk)
            return entries
        except ContentType.DoesNotExist:
            return None
    
    def get_latest(self, app_label, model, action='New', order_by='-created_at', latest='created_at'):
        e = self.get_for_model(app_label, model, action=action, order_by='-created_at')
        if e:
            return e.latest(latest)
        return None
    
    def log(self, instance, action_string=None, created=False):
        ctype = ContentType.objects.get_for_model(instance)
        if action_string:
            return self.create(object_id=instance.pk, content_type=ctype, action=self.get_status(action_string))
        if created:
            return self.create(object_id=instance.pk, content_type=ctype, action=self.get_status("New"))
        return Entry.objects.create(object_id=instance.pk, content_type=ctype, action=self.get_status("Updated"))

class Entry(models.Model):
    """
    Entry model for the logger app.
    
    This is a model that creates a generic relationship between it and
    other models for creating a "recent activity" history. It requires a global list variable in 
    the settings file named `LOGGER_MODELS`, with each value in the list being 
    in the format of `appname.model`.
    
    For example, if I have an app called `blog` and a model called `Post`
    that I want to include in my tumblelog, I would add this to my settings file.
    
    `LOGGER_MODELS = ['blog.post']`
    
    This model tries three methods for displaying the title, description,
    and title and description together on the site and in the RSS feed, and
    these methods are called `title`, `description` and `render`.
    
    It is done this way because of the way RSS displays the "title" and "description"
    separately.  If we only did a render, the RSS description of the entry
    would include both the title and the description, which would be
    undesired.
    
    There are three ways of usings these functions.
    
    1. Write a custom method in your model.
       It looks for this first, and if it doesn't find it, it moves on. It looks for 
       a method called `get_title` when getting the title, `get_description` for 
       showing the description, and `render` for displaying both the title and
       description.
       
       For example, if I have a blog app with a `Post` model, I can create a 
       `get_title`, `get_description`, and/or `render` method in my model and this 
       model will call it.
    
    2. Use a custom template.
       Inside of one of your template directories, you should have a folder for your
       app that is the name of your app.  Inside of this directory,
       create a file for the `title`, `description`, and
       `render` methods to use.  These should be named `<model_name>_title.html`, 
       `<model_name>_description.html`, and `<model_name>_render.html` respectively.
       
       For example, if I have created a blog app with a `Post` model, and I want
       to create a custom template for displaying the description, I would create
       a file `logger/post_description.html`.
       
       For the `render` method, you can use the `<model_name>_render.html`, or you
       can create a generic render template to be use by default.  Name it `render.html` 
       and put it in a folder called `logger` somewhere on your template path, 
       which will be `logger/render.html`.
       
    3. Use the default.
       This model will create generic title and description values.  If nothing
       is set for the title or description (either with a custom template or custom method),
       it will use the string representation of that object.
       
       Note: refer to the the second option above to see about creating a default
       template for the `render` method.
    """
    action = models.ForeignKey(Action, blank=True, null=True)
    created_at = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, related_name='kate_logentry')
    object_id = models.PositiveIntegerField()
    public = models.BooleanField(default=True)

    content_object = generic.GenericForeignKey()
    
    objects = EntryManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = 'Log Entries'
        get_latest_by = 'created_at'
        
    # These methods below are for displaying the entry, both on the
    # site and in the RSS feeds.  Since the RSS feeds require that
    # we display the Title and Description of an item separately,
    # we have to have separate methods for them.  We also have a 
    # render method that will display a custom render template or
    # use get_title and get_description to display one.
    
    def _get_title(self):
        """
        Here we get the title of the `Entry`. First, check for a 
        `get_title` method, then try to use a template called
        `<app_label>/<model_name>_title.html`.  If it finds neither, it
        will use the object's string representation.
        """
        # First, see if there is a title method on the content object
        if hasattr(self.content_object, 'get_title'):
            return self.content_object.get_title()
            
        # Next, see if there is template called <app_label>/<model_name>_title.html
        try:
            return render_to_string("%s/%s_title.html" % (self.content_type.app_label, self.content_type.name), 
                                    { 'obj': self.content_object })
        except TemplateDoesNotExist:
            # Finally, just use the string representation of the object
            t = Template('{{ obj }}')
            c = Context({'obj': self.content_object })
            return t.render(c)
    title = property(_get_title)
            
    def _get_description(self):
        """
        Here we get the description of the `Entry`. First, check for a 
        `get_title` method, then try to use a template called
        `<app_label>/<model_name>_title.html`.  If it finds neither, it
        will use the object's string representation.
        """
        # First, see if there is a description method on the content object
        if hasattr(self.content_object, 'get_description'):
            return self.content_object.get_description()
            
        # Next, see if there is template called <app_label>/<model_name>_description.html
        try:
            return render_to_string("%s/%s_description.html" % (self.content_type.app_label, self.content_type.name), 
                                    { 'obj': self.content_object })
        except TemplateDoesNotExist:
            # Finally, just use the string representation of the object
            t = Template('{{ obj }}')
            c = Context({ 'obj': self.content_object })
            return t.render(c)
    description = property(_get_description)

    def render(self):
        """
        This first looks for a render file under `<app_label>/<model_name>_title.html`
        and tries to use that to display this model.  If that template does
        not exist, it looks for a template called `djumblelog/render.html`, which exists
        in this app but can be replaced within another template directory.
        """
        # First, see if there is a render method on the content object
        if hasattr(self.content_object, 'render'):
            return self.content_object.render()
            
        # Next, see if there is a template called <app_label>/<model_name>_render.html
        try:
            return render_to_string("%s/%s_render.html" % (self.content_type.app_label, self.content_type.name), 
                                    { 'obj': self.content_object, 'title': self.title, 'description':  self.description})
        except TemplateDoesNotExist:
            # Finally, we use our default `render.html` template to display the entry
            return render_to_string("djumblelog/render.html", 
                                    { 'obj': self.content_object, 'title': self.title, 'description':  self.description})

    def get_absolute_url(self):
        """Use the `get_absolute_url` of the content object for our `Entry`"""
        return self.content_object.get_absolute_url()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        super(Entry, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u"%s: %s" % (self.content_type.model_class().__name__, self.content_object)

def create_entry(sender, instance, *args, **kwargs):
    """
    This is the callback that creates the `Entry` when the model has been saved.
    It uses `get_or_create` so we don't create duplicates on edit.
    """
    entry = Entry.objects.log(instance, created=kwargs['created'])
    
def delete_assoc(sender, instance, *args, **kwargs):
    """
    This deletes all the associated entries for an instance.
    """
    entries = Entry.objects.get_for_object(instance)
    if entries:
        entries.delete()
    

from django.db.models import get_model
from django.db.models.signals import post_save, pre_delete

# This loops through each of the models in LOGGER_MODELS and creates a 
# post_save signal for each of them.

try:
    for model in settings.LOGGER_MODELS:
        post_save.connect(create_entry, sender=get_model(*model.split('.')))
except AttributeError:
    pass
    
# This loops through each of the models in LOGGER_MODELS_DELETE and creates a 
# post_save signal for each of them.

try:
    for model in settings.LOGGER_MODELS_DELETE:
        pre_delete.connect(delete_assoc, sender=get_model(*model.split('.')))
except AttributeError:
    pass

