from django import forms

from katelinks.models import Category, Focus, Level

class SearchForm(forms.Form):
	keyword = forms.CharField(required=False)
	category = forms.ModelChoiceField(queryset=Category.objects.all(),
									  required=False,
									  empty_label='Any')
	level = forms.ModelChoiceField(queryset=Level.objects.all(), 
								   required=False,
								   empty_label='Any')
	focus = forms.ModelChoiceField(queryset=Focus.objects.all(),
								   required=False,
								   empty_label='Any')

	def __init__(self, *args, **kwargs):
		self.base_fields['keyword'].widget.attrs['placeholder'] = 'Keyword (optional)...'

		self.base_fields['keyword'].widget.attrs['class'] = 'span5 search-query'
		self.base_fields['category'].widget.attrs['class'] = 'span4'
		self.base_fields['level'].widget.attrs['class'] = 'span4'
		self.base_fields['focus'].widget.attrs['class'] = 'span4'

		super(SearchForm, self).__init__(*args, **kwargs)