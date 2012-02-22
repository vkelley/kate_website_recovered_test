from django.contrib.admin import widgets
from django.utils.translation import ugettext as _
from django.db.models import Q

from tick.models import *
from tick.widgets import *

from utils.check_url import check_url

class ResourceStep1Form(ModelForm):
    """
    This is the form for step 1 to the resource submission process.
    """
    class Meta:
        model = Resource
        fields = ('url', 'filename', 'title', 'description', 'source')

    def __init__(self, *args, **kwargs):
        # We set the class for title, url, and filename to text so
        # they display correctly on our page.
        self.base_fields['title'].widget.attrs['class'] = 'span5'
        self.base_fields['description'].widget.attrs['class'] = 'span5'
        self.base_fields['source'].widget.attrs['class'] = 'span5'

        self.base_fields['url'].widget.attrs['placeholder'] = 'Must begin with http://'

        super(ResourceStep1Form, self).__init__(*args, **kwargs)

    def clean_url(self):
        if self.cleaned_data['url']:
            # The URL must start with http://
            if self.cleaned_data['url'] == 'http://':
                raise forms.ValidationError(_(u'Please enter a valid URL.'))           
            # The URL must a good URL and not return a 404 code
            if not check_url(self.cleaned_data['url']):
                raise forms.ValidationError(_(u'The URL you have entered does not seem to be working.'))
            # See if the URL exists, if it does, raise an error.
            try:
                resource = Resource.objects.get(url__exact=self.cleaned_data['url'])
            except Resource.DoesNotExist:
                return self.cleaned_data['url']
            raise forms.ValidationError(_(u'This url has already been entered.'))

    def clean(self):
        # Either a URL or filename must be entered.  They can't be left
        # blank.  That's the whole reason for a resource!
        if 'url' not in self.cleaned_data and 'filename' not in self.cleaned_data:
            raise forms.ValidationError(_(u'You must enter either a URL or upload a file.'))
        return self.cleaned_data

    def save(self, user=None):
        """
        Custom save method.  Takes a ``User`` object to set as the
        creator of the resource being entered.
        """
        resource = super(ResourceStep1Form, self).save(commit=False)

        # Enter default data for the fields we exclude
        resource.entered_by = 'web'
        resource.resource_type = 'Web'
        resource.created = datetime.now()
        resource.feebased = False
        resource.published = False
        resource.disabled = False
        resource.user = user

        # Save the form data along with the m2m fields
        resource.save()
        self.save_m2m()

        return resource

class ResourceStep2Form(ModelForm):
    """
    This is the form for step 2 to the resource submission process.
    """
    class Meta:
        model = Resource
        fields = ('focus', 'sub_focus', 'tech_component', 'tech_sub_component',
                  'levels', 'content_areas', 'content_standards', 'common_core_standards')

    def __init__(self, *args, **kwargs):
        self.base_fields['content_standards'] = forms.ModelMultipleChoiceField(queryset=CoreContent.objects.none())
        self.base_fields['common_core_standards'] = forms.ModelMultipleChoiceField(queryset=CommonCoreStandard.objects.none())
        self.base_fields['content_standards'].empty_label = None
        #Before I create the form, I make tuples of the fields I want to alter.
        select_fields = ('levels', 'content_areas', 'content_standards', 'tech_sub_component', 'common_core_standards')

        # Then loop through the select fields to make changes
        # Here we change their size and their help text.
        for field in select_fields:
            self.base_fields[field].widget.attrs['size'] = 8
            self.base_fields[field].help_text = 'Hold down "Control" on a PC, or "Command" on a Mac, to select more than one.'
            self.base_fields[field].required = False

        self.base_fields['content_areas'].help_text = '<a href="http://kate.murraystate.edu/core_content/" target="_blank">Link to</a> core content.<br />' + self.base_fields['content_areas'].help_text

        # Then I create the form
        super(ResourceStep2Form, self).__init__(*args, **kwargs)

class ResourceStep3Form(ModelForm):
    """
    This is the form for step 3 to the resource submission process.
    """
    tech_standards = forms.ModelMultipleChoiceField(queryset=TechnologyStandard.objects.all())

    class Meta:
        model = Resource
        fields = ('tech_standards', 'tech_indicators')

    def __init__(self, *args, **kwargs):
        # Set the tech_standards field to use our custom widget.
        # It will display the name and description as columns.
        self.base_fields['tech_standards'].widget = CustomCheckboxSelectMultiple(
            queryset=TechnologyStandard.objects.all(), fields=('id', 'name', 'description'))

        # Set the tech_indicators to use our custom widget.  It
        # will display the standard and description as columns.
        self.base_fields['tech_indicators'].widget = CustomCheckboxSelectMultiple(
            queryset=TechIndicator.objects.all(), fields=('id', 'standard', 'description'))
        self.base_fields['tech_indicators'].label= "Kentucky's Teacher Technology Standard"    
        
        #Before I create the form, I make tuples of the fields I want to change.
        # Since it's just the fields being used, I'll use self.Meta.fields.
        select_fields = self.Meta.fields

        # Then loop through the select fields to make changes
        for field in select_fields:
            self.base_fields[field].widget.attrs['size'] = 5
            self.base_fields[field].help_text = ''
            self.base_fields[field].required = False

        # Then I create the form
        super(ResourceStep3Form, self).__init__(*args, **kwargs)

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
        self.base_fields['programs_of_studies'].help_text = '<a href="http://coekate.murraystate.edu/kate/downloads/POS_Technology_Binder.xls">Link to</a> complete statements from programs of studies.<br />' + self.base_fields['programs_of_studies'].help_text
        self.base_fields['content_areas'].help_text = '<a href="http://coekate.murraystate.edu/kate/core_content/">Link to</a> core content.<br />' + self.base_fields['content_areas'].help_text

        # Then I create the form
        super(ResourceEditForm, self).__init__(*args, **kwargs)
