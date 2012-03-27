from django import forms

from mobile_apps.models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('name', 'educational_uses', 'type', 'cost', 'levels', 'content_areas')

    def save(self, user, *args, **kwargs):
        app = super(AppForm, self).save(commit=False, *args, **kwargs)
        app.user = user
        app.save()