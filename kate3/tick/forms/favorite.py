from django import forms

from tick.models import Favorite

class FavoriteForm(forms.Form):
    """
    Form for creating and editing a favorite.
    """
    notes = forms.CharField(widget=forms.Textarea(), required=False)
    tags = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'text'}), required=False,
                           label='Keywords')

class AddFavoriteForm(FavoriteForm):
    
    def save(self, request=None, resource=None):
        """Creates the favorite and saves it"""
        favorite = Favorite.objects.create(notes=self.cleaned_data['notes'],
                                    resource=resource,
                                    user=request.user,)
        favorite.tags = self.cleaned_data['tags']

class EditFavoriteForm(FavoriteForm):
        
    def save(self, favorite):
        """Alters the favorite and saves it"""
        favorite.notes = self.cleaned_data['notes']
        favorite.tags = self.cleaned_data['tags']
        favorite.save()