from django import forms

from standards.models import Subject, Cluster, Category, Subcategory, Grade, CommonCoreStandard

class SearchForm(forms.Form):
	keyword = forms.CharField(required=False)
	standard = forms.ModelChoiceField(queryset=CommonCoreStandard.objects.all(),
											required=False,
											empty_label='Any')
	subject = forms.ModelChoiceField(queryset=Subject.objects.all(),
										required=False,
										empty_label='Any')
	grade = forms.ModelChoiceField(queryset=Grade.objects.all(),
									required=False,
									empty_label='Any')
	category = forms.ModelChoiceField(queryset=Category.objects.all(),
										required=False,
										empty_label='Any')
	subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(),
											required=False,
											empty_label='Any')
	cluster = forms.ModelChoiceField(queryset=Cluster.objects.all(),
										required=False,
										empty_label='Any')

	def __init__(self, *args, **kwargs):
		self.base_fields['keyword'].widget.attrs['placeholder'] = 'Keyword (optional)...'
		self.base_fields['keyword'].widget.attrs['class'] = 'span5 search-query'
		self.base_fields['standard'].widget.attrs['class'] = 'span4'
		self.base_fields['grade'].widget.attrs['class'] = 'span4'
		self.base_fields['subject'].widget.attrs['class'] = 'span4'
		self.base_fields['category'].widget.attrs['class'] = 'span4'
		self.base_fields['subcategory'].widget.attrs['class'] = 'span4'
		self.base_fields['cluster'].widget.attrs['class'] = 'span4'

		super(SearchForm, self).__init__(*args, **kwargs)