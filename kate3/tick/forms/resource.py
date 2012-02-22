from django.contrib.admin import widgets
from django.utils.translation import ugettext as _
from django.db.models import Q

from tick.models import *
from tick.widgets import *

from utils.check_url import check_url

class ResourceEditForm(ModelForm):
    """
    This is the form for editing a ``Resource``.  Only ``Resource``s
    that are not published can be edited.  This is somewhat of a 
    combination of steps 1, 2, 3 forms above.
    """
    tech_standards = forms.ModelMultipleChoiceField(queryset=TechnologyStandard.objects.all())

    class Meta:
        model = Resource
        exclude = ('url', 'filename',
                   'entered_by', 'created', 'user', 'resource_type',
                   'feebased', 'published', 'disabled', 'loti_level')

    def __init__(self, *args, **kwargs):
        self.base_fields['title'].widget.attrs['class'] = 'text'

        #Before I create the form, I make tuples of the fields I want to change.
        select_fields = ('levels', 'content_areas',
                         'content_standards', 'common_core_standards',
                         'tech_sub_component')

        # Then loop through the select fields to make changes
        for field in select_fields:
            self.base_fields[field].widget.attrs['size'] = 5
            self.base_fields[field].help_text = 'Hold down "Control" on a PC, or "Command" on a Mac, to select more than one.'
            self.base_fields[field].required = False
    
    
        # Set the tech_standards field to use our custom widget.
        # It will display the name and description as columns.
        self.base_fields['tech_standards'].widget = CustomCheckboxSelectMultiple(
            queryset=TechnologyStandard.objects.all(),
            fields=('id', 'name', 'description'))
        self.base_fields['tech_standards'].help_text = ''

        # Set the tech_indicators to use our custom widget.  It
        # will display the standard and description as columns.
        self.base_fields['tech_indicators'].widget = CustomCheckboxSelectMultiple(
            queryset=TechIndicator.objects.all(), fields=('id', 'standard', 'description'))
        self.base_fields['tech_indicators'].help_text = ''
        self.base_fields['tech_indicators'].label= "Kentucky's Teacher Technology Standard"

        # Alter a couple more help texts.
        self.base_fields['content_areas'].help_text = '<a href="http://coekate.murraystate.edu/kate/core_content/">Link to</a> core content.<br />' + self.base_fields['content_areas'].help_text

        # Then I create the form
        super(ResourceEditForm, self).__init__(*args, **kwargs)