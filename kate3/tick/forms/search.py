from django import forms

from core.models import ContentArea, Level
from tick.models import CommonCoreStandard, CoreContent, SubFocus

class FullSearchForm(forms.Form):
    """
    The advanced search form adds several other fields for searching on.
    """
    keyword = forms.CharField(max_length=250, 
                              widget=forms.TextInput(attrs={'class': 'span4 search-query'}),
                              required=False)
    content_areas = forms.ModelChoiceField(queryset=ContentArea.objects.all(), 
                                           required=False,
                                           empty_label='Any')
    levels = forms.ModelChoiceField(queryset=Level.objects.all(),
                                    required=False,
                                    empty_label='Any')
    content_standards = forms.ModelChoiceField(queryset=CoreContent.objects.all(), 
                                               required=False,
                                               empty_label='Any')
    common_core_standards = forms.ModelChoiceField(queryset=CommonCoreStandard.objects.all(), 
                                                   required=False,
                                                   empty_label='Any')
    sub_focus = forms.ModelChoiceField(queryset=SubFocus.objects.all(),
                                       required=False,
                                       empty_label='Any')