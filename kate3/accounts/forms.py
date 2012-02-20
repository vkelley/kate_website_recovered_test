from django import forms

from userena.forms import EditProfileForm
from userena.utils import get_profile_model

class EditFormExtra(EditProfileForm):

    class Meta:
        model = get_profile_model()
        exclude = ['user']
        fields = ['levels', 'content_areas']
        widgets = {
            'levels': forms.CheckboxSelectMultiple(),
            'content_areas': forms.CheckboxSelectMultiple(),
        }