from django import forms

from userena.forms import EditProfileForm, SignupForm
from userena.utils import get_profile_model

from core.models import ContentArea, Level

class EditFormExtra(EditProfileForm):

    class Meta:
        model = get_profile_model()
        exclude = ['user']
        fields = ['levels', 'content_areas']
        widgets = {
            'levels': forms.CheckboxSelectMultiple(),
            'content_areas': forms.CheckboxSelectMultiple(),
        }

class SignupFormExtra(SignupForm):
    levels = forms.ModelMultipleChoiceField(queryset=Level.objects.all(), 
                                            widget= forms.CheckboxSelectMultiple(),
                                            required=False)
    content_areas = forms.ModelMultipleChoiceField(queryset=ContentArea.objects.all(),
                                                   widget=forms.CheckboxSelectMultiple(),
                                                   required=False)

    def save(self):
        user = super(SignupFormExtra, self).save()

        user_profile = user.get_profile()

        for level in self.cleaned_data['levels']:
            user_profile.levels.add(level)

        for content_area in self.cleaned_data['content_areas']:
            user_profile.content_areas.add(content_area)

        user_profile.save()

        return user