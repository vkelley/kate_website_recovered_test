from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import title
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    For this widget, queryset and fields are needed.  You must specify the
    primary key column first in the fields list for it to work properly.  Refer
    to the example below.
    
    This is a custom widget built out of necessity to display checkboxes
    differently.  By default, the ``CheckboxSelectMultiple`` only displayed
    a checkbox and the unicode string for the object.  This works in most
    situations, but for our submission forms, we needed something different.
    
    This widget displays a checkbox and whatever field you tell it to.  You 
    must send a queryset and the fields being used.  
    
    For example:
    CustomCheckboxSelectMultiple(queryset=TechnologyStandard.objects.all(), fields=('id', 'name'))
    
    This above will display each row of the queryset sent, with the only column
    being the name.  Notice that the primary key column is first in the list, as
    this is a requirement.
    
    This returns a table with checkboxes for the first column, and then
    every other column listed (besides the primary key) in order.
    """
    def __init__(self, attrs=None, queryset=None, fields=()):
        super(CustomCheckboxSelectMultiple, self).__init__(attrs)
        choice_list = []
        # Make list of available choices.  There is one for each row
        # in the queryset.
        for choice in queryset:
            choice_fields = []
            # Each row will have multiple fields, displayed in columns
            # We make a list of that here
            for field in fields:
                choice_fields.append(getattr(choice, field, None))
            choice_list.append(choice_fields)
        self.choices = choice_list
        self.fields = fields

    def render(self, name, value, attrs=None):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<table><tr>']
        # Set up the table heading
        header = []
        for field in self.fields[1:]: # We don't want the ID
            header.append('<th>%s</th>' % title(field))
        output.append("".join(header))
        output.append('</tr>')
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for choice in self.choices:
            output.append('<tr>')
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], choice[0]))
            # We use a regular CheckboxInput for displaying a checkbox.
            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(choice[0])
            rendered_cb = cb.render(name, option_value)
            output.append(u'<td class="first">%s %s</td>' % (rendered_cb,
                    conditional_escape(force_unicode(choice[1]))))
            for field in choice[2:]:
                output.append('<td>%s</td>' % field)
            output.append('</tr>')
        output.append(u'</table>')
        return mark_safe(u'\n'.join(output))
